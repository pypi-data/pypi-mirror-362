# 🚨 TAREA URGENTE: Corregir Lazy Loading en Chunkers de RAG

## 📋 CONTEXTO DEL PROBLEMA

Durante una auditoría del módulo RAG del proyecto ACOLYTE, se detectó que **todos los chunkers de lenguajes violan el patrón de lazy loading**. Esto está causando que el tiempo de import del proyecto sea lento porque `tree-sitter-languages` (una librería pesada) se carga inmediatamente al importar cualquier chunker.

### Impacto actual:
- ⏱️ Tiempo de import aumentado en ~6 segundos
- 🔴 Viola los patrones establecidos en `PROMPT_PATTERNS.md`
- 📊 Afecta a 31 archivos de chunkers de lenguajes
- ⚡ El CLI y los tests cargan librerías que no necesitan

## 🎯 TU MISIÓN

Corregir UN SOLO archivo de la lista, aplicando el patrón de lazy loading correctamente. Cada IA debe:

1. **Elegir UN archivo que no esté marcado como completado**
2. **Aplicar los cambios necesarios**
3. **Marcar el archivo como completado en la checklist**
4. **NO tocar ningún otro archivo**

## 📝 PATRÓN A SEGUIR

### ❌ INCORRECTO (Import a nivel de módulo)
```python
from tree_sitter_languages import get_language  # type: ignore

class RustChunker(BaseChunker):
    def _get_tree_sitter_language(self) -> Any:
        return get_language('rust')
```

### ✅ CORRECTO (Lazy loading)
```python
# NO import a nivel de módulo

class RustChunker(BaseChunker):
    def _get_tree_sitter_language(self) -> Any:
        """Get Rust language for tree-sitter."""
        # Lazy import only when needed
        from tree_sitter_languages import get_language
        return get_language('rust')
```

## 🔧 PASOS ESPECÍFICOS

### 1. **Buscar y eliminar el import a nivel de módulo**
```python
# Buscar esta línea y ELIMINARLA:
from tree_sitter_languages import get_language  # type: ignore
```

### 2. **Modificar TODOS los métodos que usen `get_language`**

El más común es `_get_tree_sitter_language`:
```python
def _get_tree_sitter_language(self) -> Any:
    """Get [LANGUAGE] language for tree-sitter."""
    # Lazy import only when needed
    from tree_sitter_languages import get_language
    return get_language('language_name')
```

### 3. **Casos especiales a revisar**

Algunos archivos pueden tener múltiples usos de `get_language`:

#### TypeScript/JavaScript chunkers
```python
async def chunk(self, content: str, file_path: str) -> List[Chunk]:
    # ...
    if ext == 'tsx':
        # Lazy import cada vez que se necesita
        from tree_sitter_languages import get_language
        self.language = get_language('tsx')
        self.parser.set_language(self.language)
```

#### Go chunker
```python
def _categorize_imports(self, import_node: Any) -> Dict[str, List[str]]:
    # ...
    # Lazy import si usa query
    from tree_sitter_languages import get_language
    query = get_language('go').query(query_text)
```

## ⚠️ ADVERTENCIAS IMPORTANTES

1. **NO uses `if TYPE_CHECKING:`** para estos imports - necesitamos el import real en runtime
2. **CADA método debe tener su propio import** - no intentes cachear o reutilizar
3. **Mantén `# type: ignore` si estaba presente** en el import original
4. **NO modifiques la lógica** - solo mueve los imports dentro de los métodos

## 🧪 VERIFICACIÓN

Después de tus cambios, asegúrate de que:

1. **No hay imports de tree_sitter a nivel de módulo**:
   ```bash
   # No debe encontrar nada fuera de funciones/métodos
   grep -n "from tree_sitter" archivo.py | grep -v "def\|#"
   ```

2. **Cada uso de get_language tiene su import**:
   ```bash
   # Buscar todos los usos
   grep -n "get_language" archivo.py
   ```

## ✅ CHECKLIST DE ARCHIVOS

**IMPORTANTE**: Edita este archivo y marca con ✅ el archivo que completaste.

- [x] bash.py
- [x] c.py
- [ ] config_base.py
- [x] cpp.py
- [ ] csharp.py
- [x] css.py
- [ ] default.py
- [x] dockerfile.py
- [x] elisp.py
- [x] go.py
- [x] html.py
- [ ] ini.py
- [x] java.py
- [x] json.py
- [x] kotlin.py
- [x] lua.py
- [x] makefile.py
- [x] markdown.py
- [x] perl.py
- [x] php.py
- [x] python.py
- [x] r.py
- [x] ruby.py
- [x] rust.py
- [x] sql.py
- [ ] swift.py
- [x] toml.py
- [x] typescript.py
- [ ] vim.py
- [ ] xml.py
- [x] yaml.py

## 📊 PROGRESO

- **Total archivos**: 31
- **Completados**: 20
- **Pendientes**: 11
- **Porcentaje**: 64.5%

## 🔄 PROCESO DE TRABAJO

1. **Lee este documento completo**
2. **Elige UN archivo sin marcar**
3. **Aplica SOLO los cambios de lazy loading**
4. **Actualiza la checklist marcando tu archivo**
5. **Guarda y confirma tus cambios**

## 💡 EJEMPLO COMPLETO

Si eliges `rust.py`, deberías:

1. Abrir `src/acolyte/rag/chunking/languages/rust.py`
2. Eliminar: `from tree_sitter_languages import get_language`
3. Modificar el método:
   ```python
   def _get_tree_sitter_language(self) -> Any:
       """Get Rust language for tree-sitter."""
       # Lazy import only when needed
       from tree_sitter_languages import get_language
       return get_language('rust')
   ```
4. Buscar otros usos de `get_language` y aplicar el mismo patrón
5. Marcar en la checklist: `- [x] rust.py`

## 🆘 SI TIENES DUDAS

- El patrón es simple: mover el import DENTRO del método
- No cambies nada más que los imports
- Si un archivo tiene algo raro, déjalo y elige otro
- El objetivo es performance, no refactoring

---

**RECUERDA**: Solo UN archivo por IA. Esto permite trabajo paralelo sin conflictos.

**Última actualización**: 2025-01-08
