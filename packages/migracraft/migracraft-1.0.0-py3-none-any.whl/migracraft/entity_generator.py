from typing import Dict, Any, List
from pathlib import Path

class EntityGenerator:
    """Generates entity classes from schema definitions"""
    
    # Type mappings for different languages
    TYPE_MAPPINGS = {
        'typescript': {
            'SERIAL': 'number',
            'BIGSERIAL': 'number',
            'INTEGER': 'number',
            'BIGINT': 'number',
            'SMALLINT': 'number',
            'DECIMAL': 'number',
            'NUMERIC': 'number',
            'REAL': 'number',
            'DOUBLE PRECISION': 'number',
            'FLOAT4': 'number',
            'FLOAT8': 'number',
            'VARCHAR': 'string',
            'TEXT': 'string',
            'CHAR': 'string',
            'CHARACTER': 'string',
            'CHARACTER VARYING': 'string',
            'TIMESTAMP': 'Date',
            'TIMESTAMPTZ': 'Date',
            'DATE': 'Date',
            'TIME': 'string',
            'BOOLEAN': 'boolean',
            'BOOL': 'boolean',
            'JSON': 'any',
            'JSONB': 'any',
            'UUID': 'string',
            'BYTEA': 'ArrayBuffer',
        },
        'python': {
            'SERIAL': 'int',
            'BIGSERIAL': 'int',
            'INTEGER': 'int',
            'BIGINT': 'int',
            'SMALLINT': 'int',
            'DECIMAL': 'float',
            'NUMERIC': 'float',
            'REAL': 'float',
            'DOUBLE PRECISION': 'float',
            'FLOAT4': 'float',
            'FLOAT8': 'float',
            'VARCHAR': 'str',
            'TEXT': 'str',
            'CHAR': 'str',
            'CHARACTER': 'str',
            'CHARACTER VARYING': 'str',
            'TIMESTAMP': 'datetime',
            'TIMESTAMPTZ': 'datetime',
            'DATE': 'date',
            'TIME': 'time',
            'BOOLEAN': 'bool',
            'BOOL': 'bool',
            'JSON': 'dict',
            'JSONB': 'dict',
            'UUID': 'str',
            'BYTEA': 'bytes',
        },
        'dart': {
            'SERIAL': 'int',
            'BIGSERIAL': 'int',
            'INTEGER': 'int',
            'BIGINT': 'int',
            'SMALLINT': 'int',
            'DECIMAL': 'double',
            'NUMERIC': 'double',
            'REAL': 'double',
            'DOUBLE PRECISION': 'double',
            'FLOAT4': 'double',
            'FLOAT8': 'double',
            'VARCHAR': 'String',
            'TEXT': 'String',
            'CHAR': 'String',
            'CHARACTER': 'String',
            'CHARACTER VARYING': 'String',
            'TIMESTAMP': 'DateTime',
            'TIMESTAMPTZ': 'DateTime',
            'DATE': 'DateTime',
            'TIME': 'String',
            'BOOLEAN': 'bool',
            'BOOL': 'bool',
            'JSON': 'Map<String, dynamic>',
            'JSONB': 'Map<String, dynamic>',
            'UUID': 'String',
            'BYTEA': 'List<int>',
        },
        'java': {
            'SERIAL': 'Integer',
            'BIGSERIAL': 'Long',
            'INTEGER': 'Integer',
            'BIGINT': 'Long',
            'SMALLINT': 'Short',
            'DECIMAL': 'BigDecimal',
            'NUMERIC': 'BigDecimal',
            'REAL': 'Float',
            'DOUBLE PRECISION': 'Double',
            'FLOAT4': 'Float',
            'FLOAT8': 'Double',
            'VARCHAR': 'String',
            'TEXT': 'String',
            'CHAR': 'String',
            'CHARACTER': 'String',
            'CHARACTER VARYING': 'String',
            'TIMESTAMP': 'LocalDateTime',
            'TIMESTAMPTZ': 'OffsetDateTime',
            'DATE': 'LocalDate',
            'TIME': 'LocalTime',
            'BOOLEAN': 'Boolean',
            'BOOL': 'Boolean',
            'JSON': 'Object',
            'JSONB': 'Object',
            'UUID': 'UUID',
            'BYTEA': 'byte[]',
        },
        'cpp': {
            'SERIAL': 'int',
            'BIGSERIAL': 'long long',
            'INTEGER': 'int',
            'BIGINT': 'long long',
            'SMALLINT': 'short',
            'DECIMAL': 'double',
            'NUMERIC': 'double',
            'REAL': 'float',
            'DOUBLE PRECISION': 'double',
            'FLOAT4': 'float',
            'FLOAT8': 'double',
            'VARCHAR': 'std::string',
            'TEXT': 'std::string',
            'CHAR': 'std::string',
            'CHARACTER': 'std::string',
            'CHARACTER VARYING': 'std::string',
            'TIMESTAMP': 'std::chrono::system_clock::time_point',
            'TIMESTAMPTZ': 'std::chrono::system_clock::time_point',
            'DATE': 'std::chrono::system_clock::time_point',
            'TIME': 'std::string',
            'BOOLEAN': 'bool',
            'BOOL': 'bool',
            'JSON': 'std::string',
            'JSONB': 'std::string',
            'UUID': 'std::string',
            'BYTEA': 'std::vector<uint8_t>',
        },
        'csharp': {
            'SERIAL': 'int',
            'BIGSERIAL': 'long',
            'INTEGER': 'int',
            'BIGINT': 'long',
            'SMALLINT': 'short',
            'DECIMAL': 'decimal',
            'NUMERIC': 'decimal',
            'REAL': 'float',
            'DOUBLE PRECISION': 'double',
            'FLOAT4': 'float',
            'FLOAT8': 'double',
            'VARCHAR': 'string',
            'TEXT': 'string',
            'CHAR': 'string',
            'CHARACTER': 'string',
            'CHARACTER VARYING': 'string',
            'TIMESTAMP': 'DateTime',
            'TIMESTAMPTZ': 'DateTimeOffset',
            'DATE': 'DateTime',
            'TIME': 'TimeSpan',
            'BOOLEAN': 'bool',
            'BOOL': 'bool',
            'JSON': 'object',
            'JSONB': 'object',
            'UUID': 'Guid',
            'BYTEA': 'byte[]',
        },
        'go': {
            'SERIAL': 'int',
            'BIGSERIAL': 'int64',
            'INTEGER': 'int',
            'BIGINT': 'int64',
            'SMALLINT': 'int16',
            'DECIMAL': 'float64',
            'NUMERIC': 'float64',
            'REAL': 'float32',
            'DOUBLE PRECISION': 'float64',
            'FLOAT4': 'float32',
            'FLOAT8': 'float64',
            'VARCHAR': 'string',
            'TEXT': 'string',
            'CHAR': 'string',
            'CHARACTER': 'string',
            'CHARACTER VARYING': 'string',
            'TIMESTAMP': 'time.Time',
            'TIMESTAMPTZ': 'time.Time',
            'DATE': 'time.Time',
            'TIME': 'string',
            'BOOLEAN': 'bool',
            'BOOL': 'bool',
            'JSON': 'interface{}',
            'JSONB': 'interface{}',
            'UUID': 'string',
            'BYTEA': '[]byte',
        }
    }

    def __init__(self):
        pass

    def generate_entities(self, schemas: Dict[str, Any], language: str, output_dir: str) -> None:
        """Generate entity classes for all schemas in the specified language"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        for schema_name, schema_def in schemas.items():
            if 'tables' in schema_def:
                for table_name, table_def in schema_def['tables'].items():
                    entity_code = self._generate_entity(table_name, table_def, language)
                    
                    # Determine file extension
                    extensions = {
                        'typescript': '.ts',
                        'python': '.py',
                        'dart': '.dart',
                        'java': '.java',
                        'cpp': '.hpp',
                        'csharp': '.cs',
                        'go': '.go'
                    }
                    
                    file_name = f"{self._to_class_name(table_name)}{extensions[language]}"
                    file_path = output_path / file_name
                    
                    with open(file_path, 'w') as f:
                        f.write(entity_code)
                    
                    print(f"Generated {language} entity: {file_path}")

    def _generate_entity(self, table_name: str, table_def: Dict[str, Any], language: str) -> str:
        """Generate entity class for a specific table"""
        class_name = self._to_class_name(table_name)
        
        generators = {
            'typescript': self._generate_typescript_entity,
            'python': self._generate_python_entity,
            'dart': self._generate_dart_entity,
            'java': self._generate_java_entity,
            'cpp': self._generate_cpp_entity,
            'csharp': self._generate_csharp_entity,
            'go': self._generate_go_entity
        }
        
        return generators[language](class_name, table_def)

    def _generate_typescript_entity(self, class_name: str, table_def: Dict[str, Any]) -> str:
        """Generate TypeScript entity class"""
        code = f"export interface {class_name} {{\n"
        
        for column_name, column_def in table_def['columns'].items():
            ts_type = self._map_type(column_def['type'], 'typescript')
            nullable = "" if column_def.get('not_null', False) else " | null"
            code += f"  {column_name}: {ts_type}{nullable};\n"
        
        code += "}\n\n"
        
        # Generate class implementation
        code += f"export class {class_name}Entity implements {class_name} {{\n"
        
        # Properties
        for column_name, column_def in table_def['columns'].items():
            ts_type = self._map_type(column_def['type'], 'typescript')
            nullable = "" if column_def.get('not_null', False) else " | null"
            default_value = self._get_default_value(column_def, 'typescript')
            code += f"  {column_name}: {ts_type}{nullable} = {default_value};\n"
        
        # Constructor
        code += f"\n  constructor(data?: Partial<{class_name}>) {{\n"
        code += "    if (data) {\n"
        code += "      Object.assign(this, data);\n"
        code += "    }\n"
        code += "  }\n"
        
        code += "}\n"
        return code

    def _generate_python_entity(self, class_name: str, table_def: Dict[str, Any]) -> str:
        """Generate Python entity class"""
        code = "from dataclasses import dataclass\n"
        code += "from typing import Optional\n"
        code += "from datetime import datetime, date, time\n\n"
        
        code += "@dataclass\n"
        code += f"class {class_name}:\n"
        
        for column_name, column_def in table_def['columns'].items():
            py_type = self._map_type(column_def['type'], 'python')
            nullable = f"Optional[{py_type}]" if not column_def.get('not_null', False) else py_type
            default_value = self._get_default_value(column_def, 'python')
            code += f"    {column_name}: {nullable} = {default_value}\n"
        
        return code

    def _generate_dart_entity(self, class_name: str, table_def: Dict[str, Any]) -> str:
        """Generate Dart entity class"""
        code = f"class {class_name} {{\n"
        
        # Properties
        for column_name, column_def in table_def['columns'].items():
            dart_type = self._map_type(column_def['type'], 'dart')
            nullable = "?" if not column_def.get('not_null', False) else ""
            code += f"  {dart_type}{nullable} {column_name};\n"
        
        # Constructor
        code += f"\n  {class_name}({{\n"
        for column_name, column_def in table_def['columns'].items():
            required = "required " if column_def.get('not_null', False) else ""
            code += f"    {required}this.{column_name},\n"
        code += "  });\n"
        
        # fromJson method
        code += f"\n  factory {class_name}.fromJson(Map<String, dynamic> json) {{\n"
        code += f"    return {class_name}(\n"
        for column_name, column_def in table_def['columns'].items():
            dart_type = self._map_type(column_def['type'], 'dart')
            if dart_type == 'DateTime':
                code += f"      {column_name}: json['{column_name}'] != null ? DateTime.parse(json['{column_name}']) : null,\n"
            else:
                code += f"      {column_name}: json['{column_name}'],\n"
        code += "    );\n"
        code += "  }\n"
        
        # toJson method
        code += f"\n  Map<String, dynamic> toJson() {{\n"
        code += "    return {\n"
        for column_name, column_def in table_def['columns'].items():
            dart_type = self._map_type(column_def['type'], 'dart')
            if dart_type == 'DateTime':
                code += f"      '{column_name}': {column_name}?.toIso8601String(),\n"
            else:
                code += f"      '{column_name}': {column_name},\n"
        code += "    };\n"
        code += "  }\n"
        
        code += "}\n"
        return code

    def _generate_java_entity(self, class_name: str, table_def: Dict[str, Any]) -> str:
        """Generate Java entity class"""
        code = "import java.time.*;\n"
        code += "import java.math.BigDecimal;\n"
        code += "import java.util.UUID;\n\n"
        
        code += f"public class {class_name} {{\n"
        
        # Properties
        for column_name, column_def in table_def['columns'].items():
            java_type = self._map_type(column_def['type'], 'java')
            code += f"    private {java_type} {column_name};\n"
        
        # Default constructor
        code += f"\n    public {class_name}() {{}}\n"
        
        # Getters and setters
        for column_name, column_def in table_def['columns'].items():
            java_type = self._map_type(column_def['type'], 'java')
            capitalized_name = column_name.replace('_', ' ').title().replace(' ', '')
            
            # Getter
            code += f"\n    public {java_type} get{capitalized_name}() {{\n"
            code += f"        return {column_name};\n"
            code += "    }\n"
            
            # Setter
            code += f"\n    public void set{capitalized_name}({java_type} {column_name}) {{\n"
            code += f"        this.{column_name} = {column_name};\n"
            code += "    }\n"
        
        code += "}\n"
        return code

    def _generate_cpp_entity(self, class_name: str, table_def: Dict[str, Any]) -> str:
        """Generate C++ entity class"""
        code = "#pragma once\n"
        code += "#include <string>\n"
        code += "#include <vector>\n"
        code += "#include <chrono>\n\n"
        
        code += f"class {class_name} {{\n"
        code += "public:\n"
        
        # Constructor
        code += f"    {class_name}() = default;\n"
        code += f"    ~{class_name}() = default;\n\n"
        
        # Getters and setters
        for column_name, column_def in table_def['columns'].items():
            cpp_type = self._map_type(column_def['type'], 'cpp')
            
            # Getter
            code += f"    const {cpp_type}& get_{column_name}() const {{ return {column_name}_; }}\n"
            
            # Setter
            code += f"    void set_{column_name}(const {cpp_type}& value) {{ {column_name}_ = value; }}\n\n"
        
        code += "private:\n"
        
        # Private members
        for column_name, column_def in table_def['columns'].items():
            cpp_type = self._map_type(column_def['type'], 'cpp')
            code += f"    {cpp_type} {column_name}_;\n"
        
        code += "};\n"
        return code

    def _generate_csharp_entity(self, class_name: str, table_def: Dict[str, Any]) -> str:
        """Generate C# entity class"""
        code = "using System;\n\n"
        
        code += f"public class {class_name}\n{{\n"
        
        # Properties
        for column_name, column_def in table_def['columns'].items():
            cs_type = self._map_type(column_def['type'], 'csharp')
            nullable = "?" if not column_def.get('not_null', False) and cs_type not in ['string', 'object'] else ""
            property_name = column_name.replace('_', ' ').title().replace(' ', '')
            
            code += f"    public {cs_type}{nullable} {property_name} {{ get; set; }}\n"
        
        code += "}\n"
        return code

    def _generate_go_entity(self, class_name: str, table_def: Dict[str, Any]) -> str:
        """Generate Go entity struct"""
        code = "package entities\n\n"
        code += "import (\n"
        code += "    \"time\"\n"
        code += ")\n\n"
        
        code += f"type {class_name} struct {{\n"
        
        for column_name, column_def in table_def['columns'].items():
            go_type = self._map_type(column_def['type'], 'go')
            field_name = column_name.replace('_', ' ').title().replace(' ', '')
            nullable = "*" if not column_def.get('not_null', False) else ""
            json_tag = f'`json:"{column_name}"`'
            
            code += f"    {field_name} {nullable}{go_type} {json_tag}\n"
        
        code += "}\n"
        return code

    def _map_type(self, pg_type: str, language: str) -> str:
        """Map PostgreSQL type to target language type"""
        # Clean up type (remove size specifications)
        clean_type = pg_type.split('(')[0].upper()
        
        mappings = self.TYPE_MAPPINGS.get(language, {})
        return mappings.get(clean_type, 'string' if language == 'typescript' else 'str')

    def _get_default_value(self, column_def: Dict[str, Any], language: str) -> str:
        """Get default value for a column in the target language"""
        if column_def.get('not_null', False):
            defaults = {
                'typescript': {
                    'number': '0',
                    'string': "''",
                    'boolean': 'false',
                    'Date': 'new Date()',
                    'any': 'null'
                },
                'python': {
                    'int': '0',
                    'float': '0.0',
                    'str': "''",
                    'bool': 'False',
                    'datetime': 'None',
                    'date': 'None',
                    'time': 'None'
                }
            }
            pg_type = self._map_type(column_def['type'], language)
            return defaults.get(language, {}).get(pg_type, 'null' if language == 'typescript' else 'None')
        else:
            return 'null' if language == 'typescript' else 'None'

    def _to_class_name(self, table_name: str) -> str:
        """Convert table name to class name (PascalCase)"""
        return table_name.replace('_', ' ').title().replace(' ', '')