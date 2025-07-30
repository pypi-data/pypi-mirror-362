"""JavaScript/TypeScript analyzer for deep code understanding.

General Staff Role: G2 Intelligence - JavaScript/TypeScript Specialist
Provides deep analysis of JavaScript and TypeScript code to identify patterns,
complexity, and potential issues that inform AI strategic planning.

Persistent Value: Creates detailed JS/TS observations that help AI understand
modern web application architecture and make framework-aware recommendations.
"""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Set
from datetime import datetime
import logging
import os
import shlex
import atexit

from .base_analyzer import BaseAnalyzer, AnalysisResult, CodeEntity, CodeIssue, CodeMetrics


class MissingParserDependencies(Exception):
    """Raised when required JavaScript parser dependencies are missing."""
    
    def __init__(self, missing_packages: List[str], suggested_action: str = None):
        self.missing_packages = missing_packages
        self.suggested_action = suggested_action or "Install missing dependencies"
        
        package_list = ", ".join(missing_packages)
        message = f"Missing required JavaScript parser dependencies: {package_list}"
        if suggested_action:
            message += f"\nSuggested action: {suggested_action}"
        
        super().__init__(message)


class JavaScriptParseError(Exception):
    """Raised when JavaScript parsing fails."""
    
    def __init__(self, file_path: str, error_details: str, suggestion: str = None):
        self.file_path = file_path
        self.error_details = error_details
        self.suggestion = suggestion
        
        message = f"Failed to parse JavaScript file '{file_path}': {error_details}"
        if suggestion:
            message += f"\nSuggestion: {suggestion}"
            
        super().__init__(message)

logger = logging.getLogger(__name__)


class JavaScriptAnalyzer(BaseAnalyzer):
    """JavaScript analyzer using Node.js AST parsers for deep understanding.
    
    This analyzer provides intelligence about JavaScript code structure,
    patterns, and potential issues to support AI decision-making.
    Supports modern JavaScript including ES6+, JSX, and common patterns.
    """
    
    # Thresholds for AI assessment
    COMPLEXITY_THRESHOLDS = {
        'low': 5,
        'medium': 10,
        'high': 15,
        'critical': 20
    }
    
    FUNCTION_LENGTH_THRESHOLDS = {
        'acceptable': 30,
        'concerning': 50,
        'problematic': 100
    }
    
    # JS-specific patterns to detect
    CALLBACK_DEPTH_THRESHOLD = 3
    PROMISE_CHAIN_LENGTH_THRESHOLD = 5
    
    def __init__(self, dcp_path: Optional[str] = None):
        """Initialize JavaScript analyzer with DCP integration."""
        super().__init__(dcp_path)
        self._supported_languages = {'javascript', 'jsx'}
        self.parser_script = self._create_parser_script()
        self._check_node_availability()
        
    def supports_language(self, language: str) -> bool:
        """Check if analyzer supports given language."""
        return language.lower() in self._supported_languages
        
    def _check_node_availability(self):
        """Check if Node.js is available for parsing."""
        try:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                logger.warning("Node.js not available, JS analysis will be limited")
                self.node_available = False
            else:
                self.node_available = True
                logger.info(f"Using Node.js {result.stdout.strip()} for JS parsing")
        except FileNotFoundError:
            logger.warning("Node.js not found, JS analysis will be limited")
            self.node_available = False
            
    def _create_parser_script(self) -> str:
        """Create Node.js script for parsing JavaScript.
        
        Returns path to the parser script that uses @babel/parser.
        """
        # Create temporary parser script with proper cleanup
        parser_file = tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.js', 
            delete=False,
            prefix='brass_parser_'
        )
        
        # Register cleanup on exit
        atexit.register(lambda: self._cleanup_file(parser_file.name))
        
        parser_js = '''
const fs = require('fs');
const parser = require('@babel/parser');
const traverse = require('@babel/traverse').default;

// Calculate cyclomatic complexity for a function
function calculateCyclomaticComplexity(functionPath) {
    let complexity = 1; // Base complexity is 1
    
    // Traverse the function body to count decision points
    functionPath.traverse({
        // Conditional statements
        IfStatement() { complexity++; },
        ConditionalExpression() { complexity++; }, // Ternary operator
        
        // Loops
        WhileStatement() { complexity++; },
        DoWhileStatement() { complexity++; },
        ForStatement() { complexity++; },
        ForInStatement() { complexity++; },
        ForOfStatement() { complexity++; },
        
        // Switch cases
        SwitchCase(path) {
            // Don't count default case
            if (path.node.test !== null) complexity++;
        },
        
        // Logical operators (short-circuit evaluation)
        LogicalExpression(path) {
            if (path.node.operator === '&&' || path.node.operator === '||') {
                complexity++;
            }
        },
        
        // Try-catch blocks
        CatchClause() { complexity++; },
        
        // Function expressions add complexity
        FunctionExpression() { complexity++; },
        ArrowFunctionExpression() { complexity++; }
    });
    
    return complexity;
}

// Read file from command line argument
const filePath = process.argv[2];
const code = fs.readFileSync(filePath, 'utf8');

// Parse options for maximum compatibility
const parseOptions = {
    sourceType: 'unambiguous',
    plugins: [
        'jsx',
        'typescript',
        'decorators-legacy',
        'dynamicImport',
        'classProperties',
        'optionalChaining',
        'nullishCoalescingOperator',
        'asyncGenerators',
        'objectRestSpread'
    ]
};

try {
    const ast = parser.parse(code, parseOptions);
    
    const analysis = {
        entities: [],
        imports: [],
        exports: [],
        complexity: {},
        issues: [],
        metrics: {
            lines: code.split('\\n').length,
            functions: 0,
            classes: 0,
            callbacks: 0,
            promises: 0,
            asyncFunctions: 0
        },
        syntax_features: {
            jsx_elements: 0,
            typescript_annotations: 0,
            async_await: 0,
            destructuring: 0,
            arrow_functions: 0,
            template_literals: 0,
            optional_chaining: 0,
            nullish_coalescing: 0
        }
    };
    
    // Traverse AST to extract information
    traverse(ast, {
        FunctionDeclaration(path) {
            const functionName = path.node.id ? path.node.id.name : '<anonymous>';
            const complexity = calculateCyclomaticComplexity(path);
            
            analysis.entities.push({
                type: 'function',
                name: functionName,
                line_start: path.node.loc.start.line,
                line_end: path.node.loc.end.line,
                async: path.node.async,
                generator: path.node.generator,
                params: path.node.params.length,
                complexity: complexity
            });
            analysis.metrics.functions++;
            if (path.node.async) analysis.metrics.asyncFunctions++;
        },
        
        ArrowFunctionExpression(path) {
            // Check if it's a callback (nested in CallExpression)
            if (path.findParent(p => p.isCallExpression())) {
                analysis.metrics.callbacks++;
            }
            
            analysis.syntax_features.arrow_functions++;
            if (path.node.async) analysis.syntax_features.async_await++;
            
            const complexity = calculateCyclomaticComplexity(path);
            
            analysis.entities.push({
                type: 'arrow_function',
                name: '<arrow>',
                line_start: path.node.loc.start.line,
                line_end: path.node.loc.end.line,
                async: path.node.async,
                params: path.node.params.length,
                complexity: complexity
            });
        },
        
        ClassDeclaration(path) {
            const methods = path.node.body.body.filter(
                member => member.type === 'MethodDefinition'
            ).length;
            
            analysis.entities.push({
                type: 'class',
                name: path.node.id ? path.node.id.name : '<anonymous>',
                line_start: path.node.loc.start.line,
                line_end: path.node.loc.end.line,
                methods: methods,
                superClass: path.node.superClass ? true : false
            });
            analysis.metrics.classes++;
        },
        
        ImportDeclaration(path) {
            analysis.imports.push({
                source: path.node.source.value,
                line: path.node.loc.start.line
            });
        },
        
        CallExpression(path) {
            // Detect promise chains
            if (path.node.callee.property && 
                ['then', 'catch', 'finally'].includes(path.node.callee.property.name)) {
                analysis.metrics.promises++;
            }
        },
        
        // Detect console.log (potential security issue)
        MemberExpression(path) {
            if (path.node.object.name === 'console') {
                analysis.issues.push({
                    type: 'console_statement',
                    line: path.node.loc.start.line,
                    severity: 'low'
                });
            }
            
            // Optional chaining (?.)
            if (path.node.optional) {
                analysis.syntax_features.optional_chaining++;
            }
        },
        
        // JSX Elements
        JSXElement() {
            analysis.syntax_features.jsx_elements++;
        },
        
        JSXFragment() {
            analysis.syntax_features.jsx_elements++;
        },
        
        // TypeScript annotations
        TSTypeAnnotation() {
            analysis.syntax_features.typescript_annotations++;
        },
        
        TSAsExpression() {
            analysis.syntax_features.typescript_annotations++;
        },
        
        // Async/await
        AwaitExpression() {
            analysis.syntax_features.async_await++;
        },
        
        // Destructuring
        ObjectPattern() {
            analysis.syntax_features.destructuring++;
        },
        
        ArrayPattern() {
            analysis.syntax_features.destructuring++;
        },
        
        // Template literals
        TemplateLiteral() {
            analysis.syntax_features.template_literals++;
        },
        
        // Nullish coalescing (??)
        LogicalExpression(path) {
            if (path.node.operator === '??') {
                analysis.syntax_features.nullish_coalescing++;
            }
        }
    });
    
    // Calculate average cyclomatic complexity from all functions
    const complexities = analysis.entities
        .filter(entity => entity.complexity !== undefined)
        .map(entity => entity.complexity);
    
    analysis.complexity.average = complexities.length > 0 
        ? Math.round(complexities.reduce((sum, c) => sum + c, 0) / complexities.length)
        : 1;
    analysis.complexity.max = complexities.length > 0 ? Math.max(...complexities) : 1;
    analysis.complexity.min = complexities.length > 0 ? Math.min(...complexities) : 1;
    
    console.log(JSON.stringify(analysis, null, 2));
    
} catch (error) {
    console.error(JSON.stringify({
        error: error.message,
        type: 'parse_error',
        file: filePath,
        stack: error.stack,
        location: error.loc || null,
        code: error.code || null,
        reasonCode: error.reasonCode || null,
        syntaxError: error instanceof SyntaxError,
        suggestions: getSuggestions(error, filePath)
    }));
    process.exit(1);
}

// Helper function to provide parse error suggestions
function getSuggestions(error, filePath) {
    const suggestions = [];
    const errorMsg = error.message.toLowerCase();
    
    if (errorMsg.includes('jsx')) {
        suggestions.push('This file may contain JSX syntax. Ensure the file extension is .jsx or .tsx');
    }
    
    if (errorMsg.includes('typescript') || errorMsg.includes('type annotation')) {
        suggestions.push('This file may contain TypeScript syntax. Ensure the file extension is .ts or .tsx');
    }
    
    if (errorMsg.includes('unexpected token')) {
        suggestions.push('Check for syntax errors around the unexpected token location');
    }
    
    if (errorMsg.includes('import') || errorMsg.includes('export')) {
        suggestions.push('Check ES6 module syntax - ensure import/export statements are correct');
    }
    
    return suggestions;
}
        '''
        
        parser_file.write(parser_js)
        parser_file.close()
        return parser_file.name
        
    def analyze(self, file_path: Path) -> AnalysisResult:
        """Analyze JavaScript/TypeScript file for deep understanding.
        
        Args:
            file_path: Path to JS/TS file
            
        Returns:
            AnalysisResult with comprehensive JavaScript intelligence
        """
        if not self.node_available:
            return self._create_fallback_analysis(file_path)
            
        try:
            # First check if we have the required npm packages
            self._ensure_parser_dependencies()
            
            # Run parser script with secure path handling and global module access
            safe_file_path = shlex.quote(str(file_path))
            safe_parser_script = shlex.quote(self.parser_script)
            
            # Get global npm modules path for NODE_PATH
            env = os.environ.copy()
            try:
                npm_global_result = subprocess.run(
                    ['npm', 'root', '-g'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if npm_global_result.returncode == 0:
                    global_modules_path = npm_global_result.stdout.strip()
                    env['NODE_PATH'] = global_modules_path
                    logger.debug(f"Set NODE_PATH to: {global_modules_path}")
            except Exception as e:
                logger.warning(f"Could not set NODE_PATH: {e}")
            
            result = subprocess.run(
                ['node', safe_parser_script, safe_file_path],
                capture_output=True,
                text=True,
                timeout=10,
                shell=False,  # Explicitly disable shell
                env=env
            )
            
            if result.returncode != 0:
                # Enhanced error handling for parse failures
                try:
                    error_data = json.loads(result.stderr)
                    error_details = error_data.get('error', 'Unknown parse error')
                    suggestions = error_data.get('suggestions', [])
                    
                    raise JavaScriptParseError(
                        file_path=str(file_path),
                        error_details=error_details,
                        suggestion='; '.join(suggestions) if suggestions else None
                    )
                except json.JSONDecodeError:
                    # Fallback for non-JSON error output
                    logger.error(f"Parser error: {result.stderr}")
                    raise JavaScriptParseError(
                        file_path=str(file_path),
                        error_details=result.stderr,
                        suggestion="Check syntax and file encoding"
                    )
                
            # Parse the analysis results
            analysis_data = json.loads(result.stdout)
            
            # Convert to our standard format
            return self._convert_to_analysis_result(file_path, analysis_data)
            
        except MissingParserDependencies as e:
            logger.error(f"Missing parser dependencies: {e}")
            return self._create_fallback_analysis(file_path)
        except JavaScriptParseError as e:
            logger.error(f"JavaScript parse error in {e.file_path}: {e.error_details}")
            if e.suggestion:
                logger.info(f"Suggestion: {e.suggestion}")
            return self._create_fallback_analysis(file_path)
        except subprocess.TimeoutExpired:
            logger.error(f"Parser timeout for {file_path}")
            return self._create_fallback_analysis(file_path)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid parser output: {e}")
            return self._create_fallback_analysis(file_path)
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return self._create_fallback_analysis(file_path)
    def _get_global_node_modules_path(self):
        """Get the global node_modules path for NODE_PATH."""
        try:
            result = subprocess.run(['npm', 'config', 'get', 'prefix'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                prefix = result.stdout.strip()
                return f"{prefix}/lib/node_modules"
        except Exception:
            pass
        return None

    def _check_package_available(self, package_name):
        """Check if a package is available via require.resolve, with NODE_PATH support."""
        # Try without NODE_PATH first (for local packages)
        check_result = subprocess.run(
            ['node', '-e', f"require.resolve('{package_name}')"],
            capture_output=True,
            text=True
        )
        
        if check_result.returncode == 0:
            logger.debug(f"Package {package_name} found locally")
            return True
            
        # Try with NODE_PATH (for global packages)
        global_path = self._get_global_node_modules_path()
        if global_path:
            logger.info(f"Trying NODE_PATH fallback at {global_path} for {package_name}")
            env = os.environ.copy()
            env['NODE_PATH'] = global_path
            check_result = subprocess.run(
                ['node', '-e', f"require.resolve('{package_name}')"],
                capture_output=True,
                text=True,
                env=env
            )
            if check_result.returncode == 0:
                logger.info(f"Package {package_name} found via NODE_PATH")
                return True
        
        logger.debug(f"Package {package_name} not found locally or globally")
        return False

    def _get_dependency_install_method(self):
        """Determine how JavaScript parser dependencies were resolved."""
        # Check if we auto-installed during this session
        if hasattr(self, '_dependency_install_method'):
            return self._dependency_install_method
            
        required_packages = ['@babel/parser', '@babel/traverse']
        
        # Check if any packages are found locally
        local_available = []
        global_available = []
        
        for package in required_packages:
            # Check local first
            check_result = subprocess.run(
                ['node', '-e', f"require.resolve('{package}')"],
                capture_output=True, text=True
            )
            if check_result.returncode == 0:
                local_available.append(package)
                continue
                
            # Check global with NODE_PATH
            global_path = self._get_global_node_modules_path()
            if global_path:
                env = os.environ.copy()
                env['NODE_PATH'] = global_path
                check_result = subprocess.run(
                    ['node', '-e', f"require.resolve('{package}')"],
                    capture_output=True, text=True, env=env
                )
                if check_result.returncode == 0:
                    global_available.append(package)
        
        if local_available and not global_available:
            return "already-present-local"
        elif global_available and not local_available:
            return "already-present-global"
        elif local_available and global_available:
            return "already-present-mixed"
        else:
            return "not-available"

    def _ensure_parser_dependencies(self):
        """Ensure required npm packages are available with auto-install.
        
        Attempts to auto-install @babel/parser and @babel/traverse if missing.
        Falls back to setup script creation if auto-install fails.
        """
        missing_packages = []
        required_packages = ['@babel/parser', '@babel/traverse']
        
        # Check which packages are missing
        for package in required_packages:
            if not self._check_package_available(package):
                missing_packages.append(package)
        
        if not missing_packages:
            logger.debug("All required JavaScript parser dependencies are available")
            return
        
        logger.info(f"Missing JavaScript parser dependencies: {', '.join(missing_packages)}")
        
        # Attempt auto-install
        try:
            self._auto_install_dependencies(missing_packages)
            
            # Verify installation succeeded
            still_missing = []
            for package in missing_packages:
                if not self._check_package_available(package):
                    still_missing.append(package)
            
            if still_missing:
                raise MissingParserDependencies(
                    still_missing,
                    "Auto-install completed but some packages still not found. Try manual installation."
                )
            
            logger.info("Successfully auto-installed JavaScript parser dependencies")
            # Mark that dependencies were auto-installed for metadata tracking
            self._dependency_install_method = "auto-installed-global"
            
        except Exception as e:
            logger.warning(f"Auto-install failed: {e}")
            # Fall back to creating setup script
            self._create_setup_script(missing_packages)
            raise MissingParserDependencies(
                missing_packages,
                f"Auto-install failed. Please run the setup script or install manually: npm install --no-save {' '.join(missing_packages)}"
            )
    
    def _auto_install_dependencies(self, packages: List[str]):
        """Auto-install npm packages with timeout and error handling."""
        install_command = ['npm', 'install', '-g'] + packages
        
        logger.info(f"Auto-installing dependencies globally: {' '.join(packages)}")
        
        try:
            result = subprocess.run(
                install_command,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            if result.returncode != 0:
                error_msg = f"npm install failed with exit code {result.returncode}"
                if result.stderr:
                    error_msg += f": {result.stderr}"
                raise RuntimeError(error_msg)
            
            if result.stdout:
                logger.debug(f"npm install output: {result.stdout}")
                
        except subprocess.TimeoutExpired:
            raise RuntimeError("npm install timed out after 30 seconds")
        except FileNotFoundError:
            raise RuntimeError("npm command not found. Please ensure Node.js and npm are installed.")
    
    def _create_setup_script(self, packages: List[str]):
        """Create a setup script as fallback when auto-install fails."""
        try:
            setup_script = Path(self.parser_script).parent / "setup_js_parser.sh"
            setup_content = f"""#!/bin/bash
# Install JavaScript parser dependencies
npm install --no-save {' '.join(packages)}
"""
            setup_script.write_text(setup_content)
            logger.info(f"Created setup script: {setup_script}")
        except Exception as e:
            logger.error(f"Failed to create setup script: {e}")
            
    def _convert_to_analysis_result(self, file_path: Path, 
                                   parser_data: Dict[str, Any]) -> AnalysisResult:
        """Convert parser output to standard AnalysisResult.
        
        Args:
            file_path: Path to analyzed file
            parser_data: Raw parser output
            
        Returns:
            Standardized AnalysisResult
        """
        entities = []
        issues = []
        
        # Convert entities
        for entity_data in parser_data.get('entities', []):
            entity = CodeEntity(
                entity_type=entity_data['type'],
                entity_name=entity_data['name'],
                file_path=str(file_path),
                line_start=entity_data['line_start'],
                line_end=entity_data['line_end'],
                parameters=list(range(entity_data.get('params', 0))),
                metadata={
                    'is_async': entity_data.get('async', False),
                    'is_generator': entity_data.get('generator', False),
                    'is_arrow': entity_data['type'] == 'arrow_function',
                    'method_count': entity_data.get('methods', 0),
                    'has_superclass': entity_data.get('superClass', False)
                }
            )
            
            # Estimate complexity based on function length
            entity.complexity_score = max(1, (entity.line_end - entity.line_start) // 10)
            
            entities.append(entity)
            
            # Check for issues
            self._check_javascript_issues(entity, issues)
            
        # Add parser-detected issues
        for issue_data in parser_data.get('issues', []):
            issues.append(CodeIssue(
                issue_type=issue_data['type'],
                severity=issue_data['severity'],
                file_path=str(file_path),
                line_number=issue_data['line'],
                entity_name='',
                description=f"{issue_data['type'].replace('_', ' ').title()} detected",
                ai_recommendation=self._get_js_recommendation(issue_data['type']),
                fix_complexity='trivial'
            ))
            
        # Create metrics
        metrics_data = parser_data.get('metrics', {})
        metrics = CodeMetrics(
            total_lines=metrics_data.get('lines', 0),
            code_lines=int(metrics_data.get('lines', 0) * 0.8),  # Estimate
            total_entities=len(entities),
            total_functions=metrics_data.get('functions', 0),
            total_classes=metrics_data.get('classes', 0),
            average_complexity=parser_data.get('complexity', {}).get('average', 1),
            language_specific_metrics={
                'async_functions': metrics_data.get('asyncFunctions', 0),
                'callbacks': metrics_data.get('callbacks', 0),
                'promises': metrics_data.get('promises', 0),
                'uses_jsx': any('.jsx' in str(imp.get('source', '')) 
                              for imp in parser_data.get('imports', [])),
                'framework': self._detect_framework(parser_data.get('imports', [])),
                'dependency_install_method': self._get_dependency_install_method(),
                # Add syntax features from parser
                **parser_data.get('syntax_features', {})
            }
        )
        
        return AnalysisResult(
            file_path=str(file_path),
            language='javascript',
            analysis_timestamp=datetime.now(),
            entities=entities,
            issues=issues,
            metrics=metrics,
            imports=[imp['source'] for imp in parser_data.get('imports', [])],
            analysis_metadata={
                'analyzer': 'JavaScriptAnalyzer',
                'version': '1.0',
                'parser': '@babel/parser',
                'parse_success': True
            }
        )
        
    def _check_javascript_issues(self, entity: CodeEntity, issues: List[CodeIssue]):
        """Check for JavaScript-specific issues.
        
        Args:
            entity: Code entity to check
            issues: List to append issues to
        """
        # Check for long functions
        function_length = entity.line_end - entity.line_start + 1
        if function_length > self.FUNCTION_LENGTH_THRESHOLDS['problematic']:
            issues.append(CodeIssue(
                issue_type='long_function',
                severity='high',
                file_path=entity.file_path,
                line_number=entity.line_start,
                entity_name=entity.entity_name,
                description=f"Function is {function_length} lines long",
                ai_recommendation="Consider breaking into smaller functions for better testability",
                fix_complexity='moderate'
            ))
            
        # Check for callback complexity
        if entity.metadata.get('is_arrow') and entity.complexity_score > 5:
            issues.append(CodeIssue(
                issue_type='complex_callback',
                severity='medium',
                file_path=entity.file_path,
                line_number=entity.line_start,
                entity_name=entity.entity_name,
                description="Complex callback function detected",
                ai_recommendation="Consider using async/await or extracting to named function",
                fix_complexity='simple'
            ))
            
        # Check for missing async in promise-returning functions
        # (This would need more sophisticated detection in real implementation)
        
    def _detect_framework(self, imports: List[Dict[str, Any]]) -> str:
        """Detect JavaScript framework from imports with enhanced detection.
        
        Args:
            imports: List of import data
            
        Returns:
            Detected framework name
        """
        import_sources = [imp.get('source', '') for imp in imports]
        
        # React family detection
        react_indicators = ['react', 'react-dom', 'react-native', '@react-native', 'next', 'gatsby']
        if any(indicator in src for src in import_sources for indicator in react_indicators):
            return 'react'
            
        # Vue family detection  
        vue_indicators = ['vue', '@vue', 'nuxt', 'quasar']
        if any(indicator in src for src in import_sources for indicator in vue_indicators):
            return 'vue'
            
        # Angular family detection
        angular_indicators = ['@angular', '@ngrx', 'rxjs']
        if any(indicator in src for src in import_sources for indicator in angular_indicators):
            return 'angular'
            
        # Node.js backend frameworks
        backend_indicators = ['express', 'koa', 'fastify', 'nest', '@nestjs']
        if any(indicator in src for src in import_sources for indicator in backend_indicators):
            return 'backend'
            
        # Testing frameworks
        test_indicators = ['jest', 'mocha', 'chai', 'cypress', '@testing-library']
        if any(indicator in src for src in import_sources for indicator in test_indicators):
            return 'testing'
            
        # Build tools and utilities
        build_indicators = ['webpack', 'vite', 'rollup', 'parcel']
        if any(indicator in src for src in import_sources for indicator in build_indicators):
            return 'build-tool'
            
        return 'vanilla'
            
    def _get_js_recommendation(self, issue_type: str) -> str:
        """Get AI recommendation for JavaScript issue type.
        
        Args:
            issue_type: Type of issue
            
        Returns:
            Strategic recommendation for AI
        """
        recommendations = {
            'console_statement': "Remove console statements before production deployment",
            'eval_usage': "Replace eval() with safer alternatives like JSON.parse or Function constructor",
            'global_variable': "Use module pattern or ES6 modules to avoid global namespace pollution",
            'debugger_statement': "Remove debugger statements before committing",
            'alert_usage': "Replace alert() with proper UI notifications"
        }
        
        return recommendations.get(
            issue_type, 
            f"Review and fix {issue_type.replace('_', ' ')}"
        )
        
    def _create_fallback_analysis(self, file_path: Path) -> AnalysisResult:
        """Create basic analysis when Node.js parser unavailable.
        
        This provides degraded but still useful intelligence.
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            # Basic metrics
            total_lines = len(lines)
            
            # Simple pattern matching for basic intelligence
            function_count = sum(1 for line in lines 
                               if 'function' in line or '=>' in line)
            class_count = sum(1 for line in lines if 'class ' in line)
            
            # Basic issues detection
            issues = []
            for i, line in enumerate(lines, 1):
                if 'console.' in line:
                    issues.append(CodeIssue(
                        issue_type='console_statement',
                        severity='low',
                        file_path=str(file_path),
                        line_number=i,
                        entity_name='',
                        description='Console statement detected',
                        ai_recommendation='Remove console statements for production',
                        fix_complexity='trivial'
                    ))
                elif 'eval(' in line:
                    issues.append(CodeIssue(
                        issue_type='eval_usage',
                        severity='critical',
                        file_path=str(file_path),
                        line_number=i,
                        entity_name='',
                        description='Eval usage detected - security risk',
                        ai_recommendation='Replace eval with safer alternative',
                        fix_complexity='moderate'
                    ))
                    
            return AnalysisResult(
                file_path=str(file_path),
                language='javascript',
                analysis_timestamp=datetime.now(),
                entities=[],
                issues=issues,
                metrics=CodeMetrics(
                    total_lines=total_lines,
                    code_lines=int(total_lines * 0.8),
                    total_functions=function_count,
                    total_classes=class_count,
                    documentation_coverage=0.0
                ),
                analysis_metadata={
                    'analyzer': 'JavaScriptAnalyzer',
                    'version': '1.0',
                    'parser': 'fallback',
                    'parse_success': False,
                    'fallback_reason': 'Node.js unavailable'
                }
            )
            
        except Exception as e:
            logger.error(f"Fallback analysis failed: {e}")
            return AnalysisResult(
                file_path=str(file_path),
                language='javascript',
                analysis_timestamp=datetime.now(),
                entities=[],
                issues=[],
                metrics=CodeMetrics(),
                analysis_metadata={
                    'analyzer': 'JavaScriptAnalyzer',
                    'version': '1.0',
                    'error': str(e)
                }
            )
            
    def _cleanup_file(self, file_path: str):
        """Safely clean up temporary file."""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            logger.warning(f"Failed to cleanup temp file {file_path}: {e}")
    
    def __del__(self):
        """Clean up temporary parser script."""
        if hasattr(self, 'parser_script'):
            self._cleanup_file(self.parser_script)