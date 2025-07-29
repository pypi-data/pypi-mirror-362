#!/usr/bin/env python3
"""
Complete ACOLYTE configuration template
Contains ALL sections from .acolyte.example.complete
Values are filled during installation process

CHANGELOG:
- v1.0.1: Optimized concurrent_workers (max 6 for Weaviate v3 stability)
- v1.0.1: Improved worker_batch_size calculation for RAM tiers
- v1.0.1: Lowered min_files_for_parallel threshold (15 vs 20)
- v1.0.1: Enhanced parallel processing enablement logic
- v1.0.1: Better embeddings_semaphore calculation based on VRAM
"""

from typing import Dict, Any, List, Optional
from acolyte.core.utils.datetime_utils import utc_now_iso


def get_complete_config(
    project_id: str,
    project_name: str,
    project_path: str,
    project_user: str,
    project_description: str,
    ports: Dict[str, int],
    hardware: Dict[str, Any],
    model: Dict[str, Any],
    linting: Dict[str, Any],
    ignore_custom: List[str],
    docker: Dict[str, Any],
    detected_stack: Optional[Dict[str, List[str]]] = None,
    code_style: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Generate complete ACOLYTE configuration with ALL required sections.
    Based on .acolyte.example.complete

    Args:
        project_id: Unique project identifier
        project_name: User's project name
        project_path: Path to user's project
        project_user: Developer username
        project_description: Project description
        ports: Port configuration
        hardware: Detected hardware
        model: Selected model configuration
        linting: Linter configuration (detected during install)
        ignore_custom: Custom ignore patterns from user
        docker: Docker configuration
        detected_stack: Detected technology stack (optional)
        code_style: Detected code style preferences (optional)

    Returns:
        Complete configuration dictionary matching .acolyte.example.complete
    """

    # Default stack if not detected
    if detected_stack is None:
        detected_stack = {"backend": [], "frontend": [], "tools": []}

    # Default code style if not detected
    if code_style is None:
        code_style = {
            "python": {
                "formatter": "black",
                "linter": "ruff",
                "line_length": 100,
                "quotes": "double",
                "docstring_style": "google",
                "type_checking": "strict",
            },
            "javascript": {
                "formatter": "prettier",
                "linter": "eslint",
                "semicolons": False,
                "quotes": "single",
                "indent": 2,
                "typescript": True,
            },
            "general": {
                "indent_style": "spaces",
                "trim_trailing_whitespace": True,
                "insert_final_newline": True,
                "charset": "utf-8",
            },
        }

    # ============================================================================
    # INDEXING CONFIGURATION - COMPLETE OPTIMIZATION LOGIC
    # ============================================================================
    # All indexing values calculated together for perfect mathematical optimization

    # GPU VRAM detection for embeddings optimization
    gpu_vram_mb = hardware.get("gpu", {}).get("vram_mb", 0)

    # BASIC BATCH SIZES
    batch_size = 20  # Basic batch size for small datasets

    # PARALLEL PROCESSING OPTIMIZATION (mathematically optimized)
    # These values work together: 4 workers × 12 files = 48 files per complete round
    concurrent_workers = 4  # Number of parallel workers
    worker_batch_size = 12  # Files per worker batch
    large_dataset_batch_size = 48  # Batch size for large datasets (4×12=48)
    embeddings_semaphore = 2  # Max concurrent GPU operations

    # PARALLELIZATION CONTROL
    enable_parallel = True  # ALWAYS enabled for maximum performance
    min_files_for_parallel = 1  # ALWAYS activate parallel processing

    # EMBEDDINGS OPTIMIZATION (based on GPU VRAM)
    if gpu_vram_mb == 0:
        max_tokens_per_batch = 5000  # CPU fallback
    elif gpu_vram_mb < 4000:
        max_tokens_per_batch = 10000  # 4GB VRAM
    elif gpu_vram_mb < 8000:
        max_tokens_per_batch = 25000  # 8GB VRAM
    else:
        max_tokens_per_batch = 50000  # 24GB+ VRAM

    # ============================================================================

    # Log of configuration values
    auto_config_log = f"""
# CONFIGURATION VALUES (mathematically optimized):
# BASIC BATCHING: batch_size: {batch_size}
# PARALLEL OPTIMIZATION: {concurrent_workers} workers × {worker_batch_size} files = {large_dataset_batch_size} perfect distribution
# RESOURCE CONTROL: embeddings_semaphore: {embeddings_semaphore}, enable_parallel: {enable_parallel} (always on)
# ACTIVATION: min_files_for_parallel: {min_files_for_parallel} (always parallel)
# HARDWARE-BASED: max_tokens: {max_tokens_per_batch} (GPU: {gpu_vram_mb}MB VRAM)
"""

    return {
        "version": "1.0",
        "_auto_config_note": auto_config_log,
        # === USER PROJECT INFORMATION ===
        "project": {
            "name": project_name,
            "path": project_path,  # Use absolute path for Docker mounting
            "user": project_user,
            "description": project_description,
            "created": utc_now_iso(),
            "stack": detected_stack,
        },
        # Preferred code style (detected during install)
        "code_style": code_style,
        # Detected hardware (from install detection)
        "hardware": hardware,
        # === ACOLYTE CONFIGURATION ===
        # Modelo LLM
        "model": {
            "name": model.get("name", "qwen2.5-coder:3b"),
            "context_size": model.get("context_size", 32768),
        },
        # Database
        "database": {"path": "/data/acolyte.db"},  # Path inside Docker container
        # Service ports
        "ports": ports,
        # Configuración de WebSockets
        "websockets": {"max_connections": 100, "heartbeat_interval": 30, "connection_timeout": 60},
        # Configuración de embeddings (UniXcoder)
        "embeddings": {
            "cache_size": 10000,
            "device": "auto",
            "batch_size": 20,
            "max_tokens_per_batch": max_tokens_per_batch,  # Automatically adjusted based on detected VRAM
            "reranker_model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
            "reranker_batch_size": 32,
        },
        # RAG system and search
        "search": {
            "similarity_threshold": 0.7,
            "weaviate_batch_size": 100,
            "max_chunks_in_context": 10,
            "max_conversation_history": 20,
            "hybrid_weights": {"semantic": 0.7, "lexical": 0.3},
        },
        # Advanced Weaviate configuration for batch operations
        "weaviate": {
            "num_workers": 2,  # Workers internos de Weaviate para batch
            "dynamic_batching": True,  # Ajuste dinámico del tamaño de batch
            "timeout_retries": 3,  # Reintentos en caso de timeout
            "connection_error_retries": 3,  # Reintentos en caso de error de conexión
        },
        # Fuzzy matching system for lexical search
        "rag": {
            "retrieval": {
                "fuzzy_matching": {"enabled": True, "max_variations": 5, "min_term_length": 3}
            },
            "compression": {
                "enabled": True,
                "ratio": 0.7,
                "strategy": "contextual",
                "search_multiplier": 1.5,  # How many extra chunks to search for compression
                "avg_chunk_tokens": 200,  # Average tokens per chunk for estimations
                "ratios": {
                    "high_relevance": 0.9,
                    "medium_relevance": 0.6,
                    "low_relevance": 0.3,
                    "aggressive": 0.2,
                },
                "relevance_thresholds": {"high": 0.8, "medium": 0.5, "recompress": 0.3},
                "contextual": {
                    "min_chunk_size": 100,
                    "early_stop_ms": 45,
                    "broad_query_keywords": [
                        "arquitectura",
                        "completo",
                        "general",
                        "overview",
                        "estructura",
                    ],
                    "specific_query_keywords": [
                        "error",
                        "bug",
                        "función",
                        "método",
                        "variable",
                        "línea",
                    ],
                },
                "strategies": {
                    "code": {"max_comment_length": 80, "max_empty_lines": 1, "max_signatures": 10},
                    "markdown": {"section_preview_chars": 500, "max_headers": 20},
                    "config": {"max_lines": 50, "max_sections": 20},
                    "data": {"sample_rows": 5, "max_create_statements": 3},
                    "other": {"max_content_high": 2000, "max_lines_preview": 50},
                },
            },
            "enrichment": {"batch_size": 100, "timeout_seconds": 30},
        },
        # Code indexing - ALL values calculated in INDEXING CONFIGURATION block above
        "indexing": {
            # BASIC BATCH CONFIGURATION
            "batch_size": batch_size,  # Basic batch size (20)
            "large_dataset_batch_size": large_dataset_batch_size,  # Large dataset batch (48)
            "max_file_size_mb": 10,  # Maximum file size per file
            "max_reindex_files": 50,  # Maximum files to reindex in one operation
            "overlap": 0.2,  # Chunk overlap ratio (0.0-0.5)
            # PARALLEL PROCESSING CONFIGURATION (mathematically optimized)
            "concurrent_workers": concurrent_workers,  # Workers (4)
            "worker_batch_size": worker_batch_size,  # Files per worker (12)
            "embeddings_semaphore": embeddings_semaphore,  # GPU semaphore (2)
            "enable_parallel": enable_parallel,  # Always enabled (True)
            "min_files_for_parallel": min_files_for_parallel,  # Always parallel (1)
            "max_chunk_tokens": 8000,
            "min_chunk_lines": 5,
            "checkpoint_interval": 50,  # Save progress every N files
            "chunk_sizes": {
                "python": 150,
                "javascript": 150,
                "java": 100,
                "go": 100,
                "rust": 100,
                "markdown": 50,
                "default": 100,
                "batch_max_size_mb": 50,
                "max_concurrent_batches": 3,
                "chunk_size_lines": 150,
            },
            # Worker pool timeouts (configurable for different hardware capabilities)
            "enrichment_timeout": 180.0,  # 3 minutes - Git analysis and metadata extraction
            "embeddings_timeout": 240.0,  # 4 minutes - GPU model loading and inference
            "weaviate_timeout": 120.0,  # 2 minutes - Vector database insertion
            "queue_timeout": 1200.0,  # 20 minutes - Total processing timeout for all workers
        },
        # Unified cache for all modules
        "cache": {"max_size": 1000, "ttl_seconds": 3600, "save_interval": 300},
        # Optimization system ("dream")
        "optimization": {"threshold": 7.5, "auto_optimize": False},
        # Dream System - Deep analysis and optimization
        "dream": {
            "fatigue_threshold": 7.5,
            "emergency_threshold": 9.5,
            "cycle_duration_minutes": 5,
            "dream_folder_name": ".acolyte-dreams",
            "analysis": {
                "avg_tokens_per_file": 1000,
                "usable_context_ratio": 0.9,
                "chars_per_token": 4,
                "window_sizes": {
                    "32k": {
                        "strategy": "sliding_window",
                        "new_code_size": 27000,
                        "preserved_context_size": 1500,
                    },
                    "64k": {
                        "strategy": "sliding_window",
                        "new_code_size": 55000,
                        "preserved_context_size": 3000,
                    },
                    "128k+": {"strategy": "single_pass", "system_reserve": 5000},
                },
                "default_priorities": {
                    "bugs": 0.3,
                    "security": 0.25,
                    "performance": 0.2,
                    "architecture": 0.15,
                    "patterns": 0.1,
                },
            },
            "prompts_directory": None,
        },
        # Semantic System - Language processing
        "semantic": {
            "language": "es",
            "task_detection": {
                "confidence_threshold": 0.6,
                "patterns": {
                    "es": {
                        "new_task": [
                            "vamos a implementar",
                            "necesito crear",
                            "empecemos con",
                            "quiero desarrollar",
                            "hay que hacer",
                            "implementemos",
                            "agreguemos",
                        ],
                        "continuation": [
                            "sigamos con",
                            "continuemos",
                            "donde quedamos",
                            "lo que estábamos haciendo",
                            "sobre el (.+) que",
                        ],
                    },
                    "en": {
                        "new_task": [
                            "let's implement",
                            "I need to create",
                            "let's start with",
                            "I want to develop",
                            "we need to make",
                            "let's add",
                        ],
                        "continuation": [
                            "let's continue",
                            "where were we",
                            "back to",
                            "what we were doing",
                            "about the (.+) that",
                        ],
                    },
                },
            },
            "decision_detection": {
                "auto_detect": True,
                "explicit_marker": "@decision",
                "patterns": {
                    "es": [
                        "vamos a usar (\\w+)",
                        "decidí implementar",
                        "usaremos (\\w+) para",
                        "mejor (.+?) que (.+?) porque",
                    ],
                    "en": [
                        "we'll use (\\w+)",
                        "I decided to implement",
                        "we'll use (\\w+) for",
                        "(.+?) is better than (.+?) because",
                    ],
                },
            },
            "query_analysis": {
                "generation_keywords": {
                    "es": ["crea", "genera", "escribe", "implementa", "archivo completo", "hazme"],
                    "en": ["create", "generate", "write", "implement", "complete file", "make me"],
                },
                "simple_question_patterns": {
                    "es": ["^qué es", "^cómo funciona", "^para qué sirve"],
                    "en": ["^what is", "^how does", "^what's the purpose"],
                },
            },
        },
        # Logging
        "logging": {
            "level": "INFO",
            "file": ".acolyte/logs/debug.log",
            "rotation_size_mb": 10,
            "format": "timestamp | level | component | message",
            "debug_mode": False,
        },
        # Operational limits
        "limits": {
            "max_context_percentage": 0.9,
            "session_timeout_hours": 24,
            "vector_db_max_size_gb": 50,
            "max_related_sessions": 10,
            "related_sessions_chain": 5,
            "max_summary_turns": 4,
            "token_distribution": {
                "rag_chunks": 0.6,
                "conversation_history": 0.3,
                "system_prompts": 0.1,
            },
        },
        # Files and folders to ignore during indexing
        # NOTE: This is the COMPLETE list from .acolyte.example.complete + user custom
        "ignore": {
            # Version control
            "vcs": [".git/", ".svn/", ".hg/"],
            # ACOLYTE itself
            "acolyte": [".acolyte/", "ollama/", "weaviate/"],
            # Cache and temporary files
            "cache": [
                "__pycache__/",
                ".pytest_cache/",
                ".mypy_cache/",
                ".ruff_cache/",
                ".coverage",
                "htmlcov/",
                "*.pyc",
                "*.pyo",
                ".eslintcache",
                ".stylelintcache",
                ".prettiercache",
                ".parcel-cache/",
                ".webpack/",
                ".rollup.cache/",
                ".turbo/",
                ".jest/",
                ".nyc_output/",
                "coverage/",
            ],
            # Language-specific dependencies
            "dependencies": {
                "python": ["venv/", ".venv/", "*.egg-info/", "dist/", "build/"],
                "javascript": [
                    "node_modules/",
                    "bower_components/",
                    ".next/",
                    ".nuxt/",
                    ".vercel/",
                    ".netlify/",
                    ".yarn/",
                    ".pnp.js",
                    ".pnp.cjs",
                ],
                "go": ["vendor/"],
                "rust": ["target/", "debug/", "release/"],
                "java": ["target/", "out/", "build/", ".gradle/"],
                "ruby": [".bundle/", "vendor/bundle/", "tmp/"],
                "php": ["vendor/"],
            },
            # Generated documentation
            "docs": [
                "docs/_build/",
                "site/",
                ".docusaurus/",
                "_site/",
                "public/",
                ".gatsby/",
                ".vuepress/dist/",
                "_book/",
            ],
            # IDEs and editors
            "ide": [
                ".vscode/",
                ".idea/",
                ".cursor/",
                "*.swp",
                "*~",
                ".DS_Store",
                ".project",
                ".classpath",
                ".settings/",
                "nbproject/",
            ],
            # Binaries and media
            "binary": [
                "*.exe",
                "*.dll",
                "*.so",
                "*.dylib",
                "*.jar",
                "*.class",
                "*.o",
                "*.a",
                "*.wasm",
                "*.war",
                "*.ear",
                "*.app",
                "*.deb",
                "*.rpm",
            ],
            "media": [
                "*.jpg",
                "*.jpeg",
                "*.png",
                "*.gif",
                "*.mp4",
                "*.mp3",
                "*.avi",
                "*.mov",
                "*.pdf",
                "*.ico",
                "*.svg",
                "*.webp",
                "*.ttf",
                "*.woff",
                "*.woff2",
                "*.eot",
                "*.otf",
            ],
            # Data and logs
            "data": [
                "*.log",
                "*.db",
                "*.sqlite",
                "*.sqlite3",
                "data/",
                "logs/",
                "tmp/",
                "temp/",
                "*.sql.gz",
                "*.dump",
                "*.bak",
                "*.backup",
            ],
            # Sensitive configuration
            "sensitive": [
                ".env",
                ".env.*",
                "secrets.*",
                "config.local.*",
                "*.key",
                "*.pem",
                "*.cert",
                "*.p12",
                "*.pfx",
                ".secrets/",
                "credentials/",
                "private/",
            ],
            # Custom for your project (user)
            "custom": ignore_custom,
        },
        # Docker configuration (from init.py detection)
        "docker": docker,
        # Linting configuration (detected and configured during install)
        "linting": linting,
    }
