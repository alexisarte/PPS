# PPS
Prácticas Profesionales Supervisadas

## Técnicas de anonimización utilizadas
1. **Enmascaramiento de caracteres**: sustitución de caracteres por símbolos coherentes (por ejemplo, * o x). Normalmente solo se aplica a algunos caracteres del atributo. Por ejemplo, enmascarar un código postal implicaría cambiarlo de “1923” a “19xx”
2. **Seudonimización o codificación**: Se refiere a la sustitución de datos de identificación por valores inventados.
**Cuando usarlo**: se utiliza cuando los valores de los datos deben distinguirse de forma única y no se conserva ningún carácter o cualquier otra información implícita sobre los identificadores directos del atributo original.
3. **Pseudonimización adaptada para correos electrónicos**:

## Dudas
¿Si se inserta caracteres en medio de una palabra, cuenta como error?  
¿El error se debe marcar solo en el input final, en todos los inputs o a partir de donde se cambia un caracter?  
¿Marcar errores basandose en la distancia de Levenstein o solo cuando hay errores corregidos?  

## Decisiones tomadas
- Se respetan los espacios al anonimizar  
- Reemplazar errores de tipeo por un símbolo específico, de momento se usa el símbolo michi o numeral '#'  
- De los emails se anonimiza solo el texto que está antes del '@'
