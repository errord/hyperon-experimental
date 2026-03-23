---
title: MeTTa 包管理全链分析
order: 17
---

# 文档 17：包管理（MeTTa → Python → Rust）

本文档追踪 **`register-module!` / `git-module!`** 等 MeTTa 操作，经 **Python `MeTTa` / `RunContext`** 到 **Rust `pkg_mgmt` 目录、`Environment`、`RunContext::load_module`**，并说明 **`DirCatalog`、`GitCatalog`、`LocalCatalog`（`ManagedCatalog` 实现者）、`CachedRepo`** 的职责，以及 **`environment.metta` / `init.metta`** 的配置语义。

---

## 1. 特性门控

包管理代码由 Cargo feature **`pkg_mgmt`** 保护。下列 Rust 路径在 feature 关闭时可能不存在或退化：

- `lib/src/metta/runner/stdlib/package.rs` 中的 `register-module!` / `git-module!` 通过 `stdlib/mod.rs` 的 `#[cfg(feature = "pkg_mgmt")]` 注册（见 `lib/src/metta/runner/stdlib/mod.rs` 约 `71–72` 行）。
- `RunContext::load_module`、`resolve_module` 等在 `runner/mod.rs` 中同样以 `#[cfg(feature = "pkg_mgmt")]` 区分（例如 `load_module_at_path` 约 `808` 行起）。

Python 侧 `MeTTa.load_module_at_path` **始终调用** `hp.metta_load_module_at_path`；若底层库未启用 `pkg_mgmt`，行为由 Rust 编译结果决定。

---

## 2. `register-module!`（`RegisterModuleOp`）

### 2.1 MeTTa 操作：Rust 实现

文件：`lib/src/metta/runner/stdlib/package.rs`。

- 结构体持有 `Metta` 克隆：`11–22` 行。
- `execute`：`35–50` 行  
  - 用 `expect_string_like_atom` 解析路径（`hyperon_atom::gnd::str`）。  
  - 调用 **`self.metta.load_module_at_path(path, None)`**。  
  - 成功则 `unit_result()`。

```35:50:lib/src/metta/runner/stdlib/package.rs
impl CustomExecute for RegisterModuleOp {
    fn execute(&self, args: &[Atom]) -> Result<Vec<Atom>, ExecError> {
        let arg_error = "register-module! expects a file system path; use quotes if needed";
        let path = args.get(0).and_then(expect_string_like_atom).ok_or_else(|| ExecError::from(arg_error))?;
        let path = std::path::PathBuf::from(path);
        self.metta.load_module_at_path(path, None).map_err(|e| ExecError::from(e))?;
        unit_result()
    }
}
```

### 2.2 分词器注册

同文件 `113–117` 行：`register_context_dependent_tokens` 注册 `register-module!` 与 `git-module!`。

### 2.3 Python 路径

用户可直接调用 **`MeTTa.load_module_at_path`**（`python/hyperon/runner.py` `195–204` 行）→ `hp.metta_load_module_at_path` → C `metta_load_module_at_path`（`c/src/metta.rs` 约 `1094` 行起）。

MeTTa 内 `!(register-module! "...")` 与 Python API **共用** Rust `Metta::load_module_at_path` 逻辑。

---

## 3. `git-module!`（`GitModuleOp`）

### 3.1 实现要点

文件：`lib/src/metta/runner/stdlib/package.rs` `60–110` 行。

- 从参数解析 URL（`expect_string_like_atom`）。
- `mod_name_from_url(&url)` 推导模块名；失败则返回 `ExecError`（`92–95` 行）。
- 通过 **`Metta` 内部 `context` 栈** 取当前 `RunContext`（`97–98` 行，注释标明为临时 hack）。
- 使用 `context.metta.environment().specified_mods` 上的 **`loader_for_explicit_git_module(..., UpdateMode::TryFetchLatest, ...)`**（`102–105` 行）。
- 调用 **`context.get_or_init_module_with_descriptor`** 完成加载（`104` 行）。

若 `specified_mods` 为 `None`（无可用 caches 目录），返回错误（`106` 行）。

### 3.2 与 `GitCatalog` / `LocalCatalog` 的关系

`Environment::build`（`lib/src/metta/runner/environment.rs` `357–367` 行）在存在 `caches_dir` 时构造 **`specified_mods: LocalCatalog`**，并 **`push_upstream_catalog(GitCatalog::new_without_source_repo(...))`**。`git-module!` 依赖该 **`specified_mods`** 管线拉取/解析显式 Git 模块。

---

## 4. `DirCatalog`：本地目录模块目录

文件：`lib/src/metta/runner/pkg_mgmt/catalog.rs`。

### 4.1 结构

`611–620` 行：`DirCatalog { path, fmts }`，其中 `fmts: Arc<Vec<Box<dyn FsModuleFormat>>>`。

### 4.2 `lookup`

`627–654` 行：对给定模块名，按格式列表调用 `visit_modules_in_dir_using_mod_formats`，收集匹配的 **`ModuleDescriptor`**。

### 4.3 `get_loader`

`655–670` 行：再次遍历目录，找到与传入 `descriptor` 完全一致的模块后返回对应 **`ModuleLoader`**。

### 4.4 在解析流程中的使用

**`resolve_module`**（`311–379` 行）：

1. 若当前模块有 `resource_dir`，且不等于环境 `working_dir`，则构造 **`DirCatalog::new(mod_resource_dir, ...)`** 并优先搜索（`356–362` 行）。
2. 再依次搜索 **`context.metta.environment().catalogs()`** 中的目录（`365–376` 行）。

---

## 5. `GitCatalog`：基于 Git 的远程模块目录

文件：`lib/src/metta/runner/pkg_mgmt/git_catalog.rs`。

### 5.1 `ModuleGitLocation`

`16–107` 行：描述 `git_url`、`git_branch`、`git_subdir`、`git_main_file`、`local_path` 等；**`fetch_and_get_loader`**（`47–74` 行）通过 **`CachedRepo`** 更新缓存后，用 **`loader_for_module_at_path`** 在本地路径上解析模块。

### 5.2 `GitCatalog` 结构体

`168–188` 行：包含 `catalog_repo: Option<CachedRepo>`、`caches_dir`、`catalog_file_path`、内存中的 `catalog: Mutex<Option<CatalogFileFormat>>` 等。

### 5.3 与 `catalog.json` 的对应

`109–160` 行：`CatalogFileFormat` / `CatalogFileMod` 匹配远程目录中的元数据表。

---

## 6. `LocalCatalog` 与 `ManagedCatalog`

文件：`lib/src/metta/runner/pkg_mgmt/managed_catalog.rs`。

### 6.1 `ManagedCatalog` trait

`74–104` 行：定义 `clear_all`、`fetch`、`remove`、`fetch_newest_for_all`（默认实现依赖 `sync_toc` 与 `list_name_uid_pairs`）。

### 6.2 `LocalCatalog`

`119–212` 行：

- 字段：`upstream_catalogs`、`storage_dir`、`local_toc`。
- **`lookup`**（`218–236` 行）：先查本地 TOC，再按顺序查 **上游 catalogs**。
- **`get_loader`**（`237–239` 行）：默认 `UpdateMode::FetchIfMissing`。
- **`loader_for_explicit_git_module`**（`155–164` 行）：委托 **第一个上游 `GitCatalog`** 的 `register_mod`，再通过 **`get_loader_with_explicit_refresh`** 包装为本地缓存加载器。
- **`impl ManagedCatalog for LocalCatalog`**：文件后续（约 `249` 行起，本文未全量摘抄）实现主动拉取/管理。

**语义小结**：`LocalCatalog` 是「**本地安装表 + 缓存目录**」与「**一个或多个上游 `ModuleCatalog`**」的粘合层；**`GitCatalog`** 常作为上游提供远程元数据与克隆逻辑。

---

## 7. `CachedRepo`：Git 仓库缓存

文件：`lib/src/metta/runner/pkg_mgmt/git_cache.rs`。

### 7.1 结构

`31–41` 行：`CachedRepo` 保存 `repo_local_path`、`local_path`（可含 subdir）等。

### 7.2 `new`

`43–63` 行：创建父目录，计算 `local_path`。

### 7.3 `update`

`65` 行起：按 **`UpdateMode`** 执行 `git pull` 或 `clone`（`#[cfg(feature = "git")]` 分支）；无 git 特性时行为见文件内注释（`25–29` 行）。

---

## 8. 模块解析主流程：`resolve_module`

文件：`lib/src/metta/runner/pkg_mgmt/catalog.rs` **`resolve_module`**（`311–379` 行）。

### 8.1 输入

- `pkg_info: Option<&PkgInfo>`：当前模块的包描述与依赖表。
- `context: &RunContext`：用于访问 `module().resource_dir()`、`metta().environment()` 等。
- `name_path: &str`：待解析模块名路径。

### 8.2 关键分支（顺序）

1. **合法模块名**（`314–317` 行）。
2. **依赖项显式 `fs_path`**（`321–327` 行）→ 直接 **`loader_for_module_at_path`**，不再搜 catalog。
3. **依赖项含 git URL**（`329–337` 行）→ **`specified_mods.loader_for_explicit_git_module(..., FetchIfMissing, ...)`**。
4. **`PkgInfo.strict` 且无 dep 记录**（`342–348` 行）→ 返回 `Ok(None)`。
5. **资源目录 `DirCatalog`（若适用）** + **环境 `catalogs()` 迭代**（`356–376` 行）→ `lookup_newest_with_version_req` + `get_loader`。

### 8.3 `loader_for_module_at_path`

`382–406` 行：解析相对路径相对 `search_dir`；依次调用各 **`FsModuleFormat::try_path`**。

### 8.4 目录 / 单文件模块加载器

- **`DirModule`**（`446–495` 行）：`module.metta` 可选；`init_self_module` 后 `push_parser`。
- **`SingleFileModule`**（`408–444` 行）：单 `.metta` 文件。

---

## 9. `RunContext::load_module` 与 `MettaMod`

文件：`lib/src/metta/runner/mod.rs`。

- **`load_module`**（`862–878` 行）：规范化名 → 已加载则返回 `ModId` → 否则 **`load_module_parents` + `load_module_internal`**。
- **`load_module_internal`**（`910–918` 行）：在父模块上下文中调用 **`resolve_module`**，再 **`get_or_init_module_with_descriptor`**。

**`get_or_init_module_with_descriptor`**（`961–971` 行）：描述符去重 / 别名 / 新模块初始化。

---

## 10. `environment.metta` 与 `init.metta`

### 10.1 默认内嵌模板

文件：`lib/src/metta/runner/environment.rs`。

- `36–37` 行：`include_bytes!("init.default.metta")`、`include_bytes!("environment.default.metta")`。

### 10.2 `init.default.metta`

文件：`lib/src/metta/runner/init.default.metta`（全文极短）：说明该文件在每个新 runner 顶层上下文执行。

### 10.3 `environment.default.metta`

文件：`lib/src/metta/runner/environment.default.metta`：

- `#includePath`：`{$cfgdir}/modules/`（`9–11` 行）。
- `#gitCatalog`：名称、`#url`、`#refreshTime`（`13–17` 行）。

### 10.4 构建期写入磁盘

`environment.rs` `282–314` 行：若配置 `config_dir` 且允许创建，则写入默认 **`init.metta`**。

`339–355` 行：若 **`environment.metta`** 不存在则创建为默认内容，并调用 **`interpret_environment_metta`**。

### 10.5 `interpret_environment_metta`

`375–417` 行：极简解释循环（**无完整 stdlib**）；识别：

- `#includePath` → `include_path_from_cfg_atom` → 向 `env.catalogs` 推 **`DirCatalog`**（需 `pkg_mgmt`）。
- `#gitCatalog` → `git_catalog_from_cfg_atom` → 推 **`GitCatalog`**（需 `pkg_mgmt`）。

注释说明：**EnvironmentBuilder API 与文件冲突时 API 优先**（`environment.default.metta` 第 4–5 行）。

---

## 11. Python：`EnvBuilder`、include path、`load_module_at_path`

### 11.1 `MeTTa.__init__`

`python/hyperon/runner.py` `110–132` 行：

- `hp.env_builder_push_fs_module_format(env_builder, _PyFileMeTTaModFmt)`。
- `hp.env_builder_push_include_path`：`hyperon/exts` 与 `site.getsitepackages()`。

### 11.2 `RunContext.load_module`

`88–90` 行：`hp.run_context_load_module(self.c_run_context, mod_name)`。

### 11.3 C 层 Python 模块加载

`lib/src/metta/mod.rs` 中 pybind 片段（工程内嵌的 C++/Python 桥，具体路径以仓库为准）：`module_loader_load` 调用 `hyperon.runner._priv_load_module`（约 `41–52` 行，见用户环境中 `lib/src/metta/mod.rs` 若包含 pyo3 扩展）。

`python/hyperon/runner.py` `336–345` 行 **`_priv_load_module`**：`RunContext.init_self_module` + 执行 Python `loader_func(tokenizer, metta)`。

---

## 12. 从「模块名」到 `MettaMod` 的路径小结

```text
(import! 或 load_module)
    → RunContext::load_module (runner/mod.rs ~862)
    → resolve_module (pkg_mgmt/catalog.rs ~311)
        → PkgInfo.fs_path / git / strict
        → DirCatalog(resource_dir) + Environment::catalogs (DirCatalog | GitCatalog | LocalCatalog | …)
        → ModuleCatalog::lookup_newest_with_version_req + get_loader
    → ModuleLoader::load (例如 DirModule / SingleFileModule / CoreLibLoader / Python loader)
    → RunContext::init_self_module → MettaMod 放入 runner 模块表
```

---

## 13. `FsModuleFormat` 与 `DirModuleFmt` / `SingleFileModuleFmt`

`environment.rs` `316–323` 行：`EnvBuilder::build` 时将 **`SingleFileModuleFmt`** 与 **`DirModuleFmt`** 压入 `fs_mod_formats`，并 **`Arc`** 共享给各 **`DirCatalog`**。

---

## 14. 与 MeTTa `import!` 的关系（概念）

`import!` 的具体解析与 `PkgInfo` 字段 (`DepEntry`: `fs_path`、`git_location`、`version_req`) 紧密相关，定义在 **`catalog.rs`** `PkgInfo` / `DepEntry`（约 `250–293` 行）。`resolve_module` 根据这些字段决定 **走路径、走 git、或走 catalog 搜索**。

---

## 15. 错误与日志

- `register-module!` / `git-module!` 失败时返回 **`ExecError`**，最终表现为 MeTTa 求值错误路径（由解释器处理）。
- `interpret_environment_metta` 失败时 **`log::warn!`**（`352–354` 行），不阻塞整个进程。

---

## 16. 行号速查表

| 主题 | 文件 | 行号（约） |
|------|------|------------|
| `RegisterModuleOp` / `GitModuleOp` | `stdlib/package.rs` | 11–118 |
| `resolve_module` | `pkg_mgmt/catalog.rs` | 311–379 |
| `DirCatalog` | 同上 | 611–672 |
| `loader_for_module_at_path` | 同上 | 382–406 |
| `DirModule` / `SingleFileModule` | 同上 | 408–495 |
| `ModuleCatalog` trait | 同上 | 94–190 |
| `ModuleGitLocation` / `fetch_and_get_loader` | `git_catalog.rs` | 16–107 |
| `GitCatalog` struct | 同上 | 168–188 |
| `ManagedCatalog` / `LocalCatalog` | `managed_catalog.rs` | 44–250+ |
| `CachedRepo` | `git_cache.rs` | 31–120+ |
| `environment.metta` 解释 | `environment.rs` | 375–417 |
| 默认 `environment.metta` / `init.metta` | `environment.default.metta` / `init.default.metta` | 全文 |
| `RunContext::load_module` | `runner/mod.rs` | 862–918 |
| Python `load_module_at_path` | `python/hyperon/runner.py` | 195–204 |
| C `metta_load_module_at_path` | `c/src/metta.rs` | 1094+ |

---

## 17. 设计注释（只读理解）

`builtin_mods/catalog.rs` 文件顶部注释（约 `32–49` 行）讨论 **`DirCatalog` 与 `LocalCatalog` 的差异**（只读 vs 可管理、列表能力等），有助于理解为何显式 git 模块走 **`specified_mods`（LocalCatalog）** 而非普通 include **`DirCatalog`**。

---

## 18. 测试建议

- 使用 **`EnvBuilder::test_env()`**（`environment.rs` `158–164` 行）时：**不读写配置文件**；`git-module!` 依赖的 **`caches_dir` / specified_mods** 可能与默认环境不同，需在集成测试中显式构造 `EnvBuilder`。

---

## 19. 小结

- **`register-module!`** 是对 **`Metta::load_module_at_path`** 的薄封装，绕过 catalog 名称解析，直接按路径尝试所有 **`FsModuleFormat`**。
- **`git-module!`** 依赖 **`Environment::specified_mods`**（**`LocalCatalog` + 上游 `GitCatalog`**）及当前 **`RunContext`** 的全局栈；用于显式按 URL 拉取模块。
- **常规模块名导入**走 **`resolve_module`**：**资源目录 `DirCatalog` 优先**，然后 **`Environment::catalogs()`**（由 **`environment.metta`** 与环境构建器共同填充）。
- **`CachedRepo`** 实现 **磁盘缓存与 git 同步**，被 **`ModuleGitLocation::fetch_and_get_loader`** 与 **`GitCatalog`** 使用。
- **`environment.metta` / `init.metta`** 由 **`Environment`** 构建逻辑创建/加载；前者配置 **include 路径与 git 目录**，后者在每个 runner 初始化时执行。

---

## 附录 A：`Metta::load_module_at_path`（Rust 公共 API）

`lib/src/metta/runner/mod.rs` 中 **`Metta::load_module_at_path`**（需 `pkg_mgmt`）与 **`RunContext::load_module_at_path`**（约 `808–835` 行）共享「格式尝试 → `get_or_init_module_with_descriptor`」流程。`RegisterModuleOp` 直接调用 **`self.metta.load_module_at_path`**（`package.rs` `47` 行），因此与 **Python `MeTTa.load_module_at_path`** 语义对齐。

---

## 附录 B：C API `metta_load_module_at_path`

`c/src/metta.rs` `1094–1100` 行起：`metta_load_module_at_path` 清空错误串、借用 Rust `Metta`、解析路径与可选名，失败时写入 **`metta.err_string`**。Python `runner.py` `200–203` 行在 **`mod_id`** 返回后检查 **`metta_err_str`**。

---

## 附录 C：`#includePath` 与环境目录

`environment.rs` `397–405` 行：从 `environment.metta` 解析到 **`#includePath`** 时调用 **`include_path_from_cfg_atom`**（函数定义在同文件稍后位置），向 **`env.catalogs`** 追加 **`DirCatalog`**。宏占位符 **`{$cfgdir}`** 在解释阶段展开为实际配置根路径，使 **用户模块目录** 成为 catalog 搜索的一部分。

---

## 附录 D：`#gitCatalog` 与 `git_catalog_from_cfg_atom`

`environment.rs` `407–412` 行：识别 **`#gitCatalog`** 后调用 **`git_catalog_from_cfg_atom`**（`419` 行起）。该函数读取子表达式中的 **`#name` / `#url` / `#refreshTime`**（`426–444` 行），在 **`caches_dir`** 下构造 **`GitCatalog`**（具体构造逻辑见 `445` 行之后）。这样 **远程模块目录** 与 **本地 `DirCatalog` 包含路径** 一并进入 **`Environment::catalogs()`** 迭代顺序。

---

## 附录 E：`EnvBuilder::build` 中 `working_dir` 优先权

`environment.rs` `276–280` 行：若 **`working_dir`** 存在，则在 **`proto_catalogs` 最前插入** 其路径。随后 `325–336` 行转为 **`DirCatalog`**。因此 **当前工作目录**（环境意义下）中的裸模块名解析，往往优先于仅出现在深层 include 路径中的同名模块——具体仍受 **`resolve_module` 与版本约束**影响。

---

## 附录 F：`specified_mods` 与 `GitCatalog::new_without_source_repo`

`environment.rs` `359–366` 行：在 **`caches_dir`** 存在时创建 **`LocalCatalog::new(caches_dir, "specified-mods")`**，并 **`push_upstream_catalog(GitCatalog::new_without_source_repo(...))`**。该对象与 **`git-module!`**、**依赖项中的 git URL**（`resolve_module` `329–337` 行）共用 **「显式 git 拉取」**通道，而 **非** 普通 `import!` 仅目录扫描。

---

## 附录 G：`mod_name_from_url`

`git-module!` 使用 **`mod_name_from_url`**（`package.rs` `92–95` 行）从 URL 推导模块名；该函数在 **`crate::metta::runner`** 中导出（与 `GitModuleOp` 同 use 块 `6–8` 行）。若 URL 形态非常规导致 **`None`**，操作返回 **ExecError**。

---

## 附录 H：`FsModuleFormat::paths_for_name` 契约

`catalog.rs` `504–508` 行文档：**允许返回无效路径**，由 **`try_path`** 过滤。`SingleFileModuleFmt::paths_for_name`（`529–533` 行）同时尝试 **无扩展名路径** 与 **`.metta` 扩展路径**；`DirModuleFmt`（`561–564` 行）仅拼接 **子目录名**。

---

## 附录 I：`visit_modules_in_dir_using_mod_formats`

`DirCatalog::lookup`（`647–651` 行）依赖该工具函数在目录内按格式探测模块；实现细节在同文件后部（未在正文摘全）。理解要点：**同一模块名**可能命中 **多种格式候选**，描述符区分 **`fmt_id` 与路径**。

---

## 附录 J：Python `RunContext.load_module` 与 C

`python/hyperon/runner.py` `88–90` 行：**`hp.run_context_load_module(self.c_run_context, mod_name)`**。对应 C API 由 `c/src/metta.rs` 中 **`run_context_load_module`** 导出（符号名以头文件为准），内部进入与 **`resolve_module`** 相同的 **Rust `RunContext::load_module`** 路径。

---

## 附录 K：`ModuleDescriptor` 与去重

`RunContext::get_or_init_module_with_descriptor`（`runner/mod.rs` `961–971` 行）：若描述符已存在则 **别名加载**，避免重复克隆相同内容。对 **Git 模块**，`ModuleGitLocation::uid`（`git_catalog.rs` `81–97` 行）参与 **唯一性**。

---

## 附录 L：`DirModule` 与 `module.metta` 可选性

`catalog.rs` `469–483` 行：目录模块 **可无 `module.metta`**，此时模块作为 **纯资源容器**；`open_file` 失败不视为致命，**仅跳过 push_parser**。这与 **测试资源目录**、**多媒体资产包** 用法一致。

---

## 附录 M：`register-module!` 与 catalog 的关系

`register-module!` **不经过 `resolve_module` 名称解析**；它直接 **`load_module_at_path`**。适用于 **已知绝对/相对路径** 的脚本化加载；而 **`import!`** 依赖 **PkgInfo + catalogs**。

---

## 附录 N：文档与代码交叉引用

- 用户向导读：`docs/modules_dev.md` 中 **DirCatalog** 章节（与实现一致）。
- 引擎侧总览：`project_docs/output/docs/rust-engine/pkg-mgmt-catalog.md`（若存在于工作区）。

---

## 附录 O：`PkgInfo` 与 `DepEntry` 字段心智图

`catalog.rs` `250–293` 行（节选上下文）：**`PkgInfo`** 含 **`deps: BTreeMap<String, DepEntry>`**、**`strict`**、**`version`**、**`name`** 等。**`DepEntry`** 合并 **`fs_path`** 与 **`#[serde(flatten)] git_location: ModuleGitLocation`** 以及 **`version_req`**。**`resolve_module`** 首先查 **`deps.get(mod_name)`**；无记录且 **`strict`** 时 **立即 `Ok(None)`**（`342–348` 行），体现 **「显式依赖」**策略。

---

## 附录 P：`UpdateMode` 枚举语义对照

`managed_catalog.rs` `44–57` 行：

- **`FetchIfMissing`**：无本地则拉取，有则不动。
- **`TryFetchIfOlderThan(u64)`**：缓存旧于阈值则尝试更新。
- **`TryFetchLatest`**：尝试最新，网络失败则软降级。
- **`FetchLatest`**：必须成功更新，否则错误。

**`promote_to`**（`59–71` 行）：合并两模式时取 **更激进**者，用于组合嵌套拉取策略。

---

## 附录 Q：`GitModuleOp` 与 `UpdateMode::TryFetchLatest`

`package.rs` `102–105` 行：`loader_for_explicit_git_module(..., UpdateMode::TryFetchLatest, ...)`。与 **`resolve_module`** 中依赖 git 路径使用的 **`FetchIfMissing`**（`332` 行）**不同**：**`git-module!`** 更倾向 **刷新远端**，符合 REPL / 显式用户指令语义。

---

## 附录 R：`CachedRepo::repo_local_path` 与 `local_path`

`git_cache.rs` `31–41` 行：`repo_local_path` 为 **裸仓库根**；`local_path` 可含 **subdir**。**`ModuleGitLocation::fetch_and_get_loader`**（`git_catalog.rs` `57–60` 行）在存在 **`git_main_file`** 时拼 **单文件模块路径**。

---

## 附录 S：`catalog.json` 中版本与 uid

`git_catalog.rs` `116–125` 行：**`find_mods_with_name`** 为每个 **`CatalogFileMod`** 计算 **`git_location.uid()`** 并生成 **`ModuleDescriptor`**。**`find_mod_with_descriptor`**（`128–140` 行）同时匹配 **semver version** 与 **uid**，防止 **同名不同源** 冲突。

---

## 附录 T：`LocalCatalogLoader`（概念）

`managed_catalog.rs` `208–210` 行：`get_loader_with_explicit_refresh` 返回 **`Box::new(LocalCatalogLoader { local_cache_dir, upstream_loader, update_mode })`**（结构体定义在同文件更前或更后）。该包装器负责 **把上游 loader 的结果同步到本地 TOC 目录**，抽象了 **「下载一次、多次加载」**。

---

## 附录 U：`RunContext` 全局栈与 `GitModuleOp`

`package.rs` `62–64`、`97–98` 行注释：**`GitModuleOp`** 持有 **`Arc<Mutex<Vec<...RunContext...>>>>`**，从 **`metta.0.context`** 克隆，为 **临时 hack**；与 **`RunnerState::run_in_context`**（`runner/mod.rs` `631–644` 行）推送上下文相对应。多线程并发执行 MeTTa 时存在 **UB 风险**（注释 `631–632` 行）。

---

## 附录 V：`include_path_from_cfg_atom` 行为摘要

`environment.rs` 中 **`include_path_from_cfg_atom`**（实现位于 `397` 行引用之后）：将 **`#includePath`** 子表达式转为 **磁盘路径**，并包装为 **`DirCatalog::new`**。**失败**时返回 **`Err(String)`** 由 **`interpret_environment_metta`** 向上传播。

---

## 附录 W：`Metta` 初始化与 `init.metta` 运行时机

`init.metta` 路径由 **`Environment::initialization_metta_file_path`**（`environment.rs` `74–77` 行）暴露；具体 **何时被 runner 执行** 见 **`Metta::new` / 模块初始化** 相关代码路径（`runner` 初始化序列）。本文档不展开完整时序，读者可用 **`rg init_metta_path`** 在 `lib/src/metta/runner` 内追踪。

---

## 附录 X：`register-module!` 参数仅为路径

`package.rs` `42–46` 行注释：**未来 varargs** 可能允许 **别名模块名**；当前 **忽略** `mod_name` 覆盖，**描述符名称**来自 **格式层**（`loader_for_module_at_path` / `ModuleDescriptor`）。

---

*（若 `pkg_mgmt` 或 `git` 特性关闭，请以实际 `cargo` 特性为准核对符号是否存在。）*
