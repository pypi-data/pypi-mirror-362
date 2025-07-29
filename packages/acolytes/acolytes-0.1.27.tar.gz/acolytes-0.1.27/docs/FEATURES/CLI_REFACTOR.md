## **�� CONSEJOS DE REFACTORIZACIÓN PARA CLI.PY**

### **1. SEPARACIÓN DE RESPONSABILIDADES**

**Problema actual**: El archivo tiene 1,744 líneas y mezcla muchas responsabilidades.

**Solución**: Dividir en módulos especializados:

```
src/acolyte/cli/
├── __init__.py
├── commands/
│   ├── __init__.py
│   ├── start.py      # Comando start (líneas 520-794)
│   ├── install.py    # Comando install (líneas 468-519)
│   ├── init.py       # Comando init (líneas 412-467)
│   ├── index.py      # Comando index (líneas 920-1085)
│   └── ...
├── core/
│   ├── __init__.py
│   ├── project_manager.py  # Clase ProjectManager
│   ├── docker_utils.py     # Funciones Docker
│   └── model_manager.py    # Gestión de modelos
└── utils/
    ├── __init__.py
    ├── validation.py       # Validaciones
    └── health_checks.py    # Health checks
```

### **2. EXTRACCIÓN DE LA CLASE PROJECTMANAGER**

**Problema**: La clase está mezclada con la lógica CLI.

**Solución**: Mover a `src/acolyte/core/project_manager.py`:

```python
# src/acolyte/core/project_manager.py
class ProjectManager:
    """Manages ACOLYTE projects and their configurations"""
    # Mover toda la lógica aquí
```

### **3. CREACIÓN DE UN MÓDULO DE GESTIÓN DE MODELOS**

**Problema**: La función `ensure_acolyte_model_exists` está aislada.

**Solución**: Crear `src/acolyte/core/model_manager.py`:

```python
# src/acolyte/core/model_manager.py
class ModelManager:
    def __init__(self, config: Dict[str, Any], infra_dir: Path):
        self.config = config
        self.infra_dir = infra_dir
    
    def ensure_model_exists(self, console) -> bool:
        """Ensure the acolyte model exists in Ollama"""
        # Lógica actual de ensure_acolyte_model_exists
    
    def check_model_status(self) -> Dict[str, Any]:
        """Check model status and return details"""
    
    def create_model(self, console) -> bool:
        """Create the acolyte model"""
    
    def pull_base_model(self, model_name: str, console) -> bool:
        """Pull base model if needed"""
```

### **4. REFACTORIZACIÓN DEL COMANDO START**

**Problema**: El comando `start` tiene 274 líneas y es muy complejo.

**Solución**: Dividir en clases especializadas:

```python
# src/acolyte/cli/commands/start.py
class ServiceStarter:
    def __init__(self, config: Dict[str, Any], project_dir: Path):
        self.config = config
        self.project_dir = project_dir
        self.console = Console()
    
    def start_services(self) -> bool:
        """Main entry point for starting services"""
        try:
            self._stop_existing_containers()
            self._start_docker_services()
            self._wait_for_services()
            self._ensure_model_exists()
            self._wait_for_backend()
            return True
        except Exception as e:
            self.console.print(f"[bold red]✗ Error: {e}[/bold red]")
            return False
    
    def _stop_existing_containers(self):
        """Stop existing containers"""
    
    def _start_docker_services(self):
        """Start Docker services"""
    
    def _wait_for_services(self):
        """Wait for Weaviate and Ollama"""
    
    def _ensure_model_exists(self):
        """Ensure acolyte model exists"""
    
    def _wait_for_backend(self):
        """Wait for backend to be ready"""
```

### **5. CREACIÓN DE UN MÓDULO DE VALIDACIONES**

**Problema**: Las validaciones están dispersas por todo el código.

**Solución**: Crear `src/acolyte/cli/utils/validation.py`:

```python
# src/acolyte/cli/utils/validation.py
class ProjectValidator:
    @staticmethod
    def validate_project_initialized(project_path: Path) -> bool:
        """Validate project is initialized"""
    
    @staticmethod
    def validate_project_configured(project_dir: Path) -> bool:
        """Validate project is configured"""
    
    @staticmethod
    def validate_docker_available() -> bool:
        """Validate Docker is available"""
    
    @staticmethod
    def validate_docker_compose_files(infra_dir: Path) -> bool:
        """Validate Docker Compose files exist"""
```

### **6. IMPLEMENTACIÓN DE PATRÓN COMMAND**

**Problema**: Los comandos están definidos como funciones simples.

**Solución**: Usar clases para los comandos:

```python
# src/acolyte/cli/commands/base.py
from abc import ABC, abstractmethod

class BaseCommand(ABC):
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.manager = ProjectManager()
    
    @abstractmethod
    def execute(self) -> bool:
        """Execute the command"""
        pass
    
    def validate(self) -> bool:
        """Validate prerequisites"""
        pass

# src/acolyte/cli/commands/start.py
class StartCommand(BaseCommand):
    def execute(self) -> bool:
        starter = ServiceStarter(self.config, self.project_dir)
        return starter.start_services()
```

### **7. IMPLEMENTACIÓN DE CONFIGURACIÓN CENTRALIZADA**

**Problema**: La configuración se carga en múltiples lugares.

**Solución**: Crear un gestor de configuración:

```python
# src/acolyte/core/config_manager.py
class ConfigManager:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.manager = ProjectManager()
    
    def load_config(self) -> Dict[str, Any]:
        """Load project configuration"""
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration"""
    
    def get_ports(self) -> Dict[str, int]:
        """Get service ports"""
    
    def get_model_config(self) -> Dict[str, Any]:
        """Get model configuration"""
```

### **8. IMPLEMENTACIÓN DE LOGGING ESTRUCTURADO**

**Problema**: El logging está mezclado con prints de consola.

**Solución**: Usar logging estructurado:

```python
# src/acolyte/cli/utils/logging.py
import structlog

logger = structlog.get_logger()

class ConsoleLogger:
    def __init__(self, console):
        self.console = console
    
    def info(self, message: str):
        self.console.print(f"[cyan]ℹ[/cyan] {message}")
        logger.info(message)
    
    def success(self, message: str):
        self.console.print(f"[green]✓[/green] {message}")
        logger.info(message)
    
    def error(self, message: str):
        self.console.print(f"[bold red]✗[/bold red] {message}")
        logger.error(message)
```

### **9. IMPLEMENTACIÓN DE TESTS UNITARIOS**

**Problema**: El código es difícil de testear.

**Solución**: Crear tests para cada módulo:

```python
# tests/cli/test_project_manager.py
def test_project_manager_initialization():
    manager = ProjectManager()
    assert manager.global_dir.exists()

# tests/cli/test_model_manager.py
def test_model_creation():
    manager = ModelManager(config, infra_dir)
    assert manager.ensure_model_exists(console)
```

### **10. IMPLEMENTACIÓN DE TIPOS ESTRICTOS**

**Problema**: Falta tipado estricto en muchas funciones.

**Solución**: Agregar tipos completos:

```python
from typing import Protocol, TypedDict

class ServiceConfig(TypedDict):
    ports: Dict[str, int]
    model: Dict[str, Any]
    docker: Dict[str, Any]

class ModelManagerProtocol(Protocol):
    def ensure_model_exists(self, console: Console) -> bool: ...
    def check_model_status(self) -> Dict[str, Any]: ...
```

## **�� PLAN DE REFACTORIZACIÓN RECOMENDADO**

### **FASE 1: Extracción de módulos core**
1. Mover `ProjectManager` a `core/project_manager.py`
2. Crear `core/model_manager.py`
3. Crear `core/config_manager.py`

### **FASE 2: Refactorización de comandos**
1. Crear estructura de comandos
2. Refactorizar comando `start`
3. Refactorizar otros comandos

### **FASE 3: Mejoras de utilidades**
1. Crear módulo de validaciones
2. Implementar logging estructurado
3. Agregar tipos estrictos

### **FASE 4: Tests y documentación**
1. Crear tests unitarios
2. Documentar APIs
3. Crear ejemplos de uso

## **🎯 BENEFICIOS DE LA REFACTORIZACIÓN**

1. **Mantenibilidad**: Código más fácil de mantener
2. **Testabilidad**: Cada módulo se puede testear independientemente
3. **Reutilización**: Módulos se pueden reutilizar
4. **Legibilidad**: Código más claro y organizado
5. **Escalabilidad**: Fácil agregar nuevos comandos

¿Te interesa que implemente alguna de estas refactorizaciones específicas?