# Documentación del Proyecto de Anonimización de Dataset de Interacciones

## Introducción
Este proyecto tiene como objetivo anonimizar un dataset que captura interacciones de usuario en interfaces, preservando características esenciales como la longitud de los textos ingresados y los patrones de interacción. Este enfoque permite el uso posterior del dataset para análisis sin comprometer la privacidad de los usuarios.

---

## Técnicas de Anonimización Utilizadas

### 1. Enmascaramiento de Caracteres
**Descripción**: Sustitución de caracteres originales por símbolos, manteniendo la longitud del texto.  
**Ejemplo**:  
- Original: `1923`  
- Anonimizado: `19xx`

**Adaptaciones**:  
- Se enmascaran solo caracteres sensibles (como números de teléfonos o tarjetas de crédito) sin alterar la estructura del dato.  
- Los símbolos de reemplazo (`*` o similares) se eligen para preservar la longitud y usabilidad del dato anonimizado.

---

### 2. Seudonimización
**Descripción**: Reemplazo de datos identificables con valores ficticios que no permiten la identificación directa.  
**Ejemplo**:  
- Nombre original: `Carlos`  
- Anonimizado: `Xbgmop`

**Adaptaciones**:  
- Se genera un valor aleatorio para cada palabra o dato identificado como sensible, respetando la longitud del dato original.  
- La seudonimización no es reversible para garantizar la seguridad, salvo en datos categóricos que se distinguen por su contexto.

---

### 3. Seudonimización Adaptada para Correos Electrónicos
**Descripción**: Anonimización de correos electrónicos manteniendo el dominio intacto para preservar información útil.  
**Ejemplo**:  
- Original: `usuario@ejemplo.com`  
- Anonimizado: `asdfasd@ejemplo.com`

**Adaptaciones**:  
- Solo se anonimiza la parte anterior al `@`, generando un valor aleatorio con la misma longitud que el texto original.  
- El dominio del correo se mantiene para conservar información contextual sobre la fuente del dato.

---

## Consideraciones de Usabilidad

1. **Preservación de la Longitud de los Datos**  
   - En todas las técnicas aplicadas, se respeta la longitud del texto original para que las características relacionadas con la estructura del dato sean utilizables en análisis posteriores.

2. **Detección y Marcado de Errores**  
   - Se implementa un sistema que detecta errores de tipeo en entradas intermedias durante las interacciones del usuario.
   - Los errores detectados se marcan con un símbolo específico (`#`) para identificar la posición de los cambios sin eliminar la información de interacción.

3. **Espacios y Puntuación**  
   - Los espacios entre palabras y otros separadores (como puntos o guiones) se respetan para mantener el formato original del texto.

---

## Desafíos y Soluciones Implementadas

### 1. Errores en la Entrada de Texto
   - **Desafío**: Durante la captura de interacción, los usuarios pueden cometer errores de tipeo que corrigen posteriormente.  
   - **Solución**: Los errores corregidos se marcan con un símbolo especial (`#`) para reflejar cambios sin distorsionar la información anonimizada.

### 2. Datos Mixtos (Texto y Números)
   - **Desafío**: Algunos datos contienen combinaciones de texto y números, como códigos postales o identificadores.  
   - **Solución**: Los números se enmascaran parcialmente, mientras que el texto asociado se anonimiza usando seudónimos.

### 3. Preservación del Contexto de Interacción
   - **Desafío**: El dataset se utiliza para analizar patrones de interacción y comportamiento, por lo que la anonimización no debe afectar la utilidad de los datos.  
   - **Solución**: Se preservan elementos como longitud, espacios, y estructura general del texto, mientras se anonimizan los valores específicos.

---

## Decisiones Clave en el Diseño del Sistema

1. **Marcado de Errores**  
   - Los errores detectados se marcan con `#` en lugar de eliminarse para garantizar que las correcciones sean visibles en los datos anonimizados.

2. **Estrategia de Anonimización por Categoría**  
   - Correos electrónicos: Anonimización parcial (solo antes del `@`).  
   - Números telefónicos y de tarjetas: Enmascaramiento completo.  
   - Nombres propios: Seudonimización basada en modelos de lenguaje como SpaCy y NLTK.  

3. **Adaptación de las Técnicas**  
   - Se modificaron técnicas estándar para equilibrar anonimización y usabilidad, priorizando la preservación de patrones relevantes en los datos.

---

## Conclusión
Este proyecto implementa un enfoque híbrido de anonimización adaptado a datasets de interacciones de usuario, donde la preservación de la estructura y longitud de los datos es esencial. Las técnicas utilizadas, junto con las adaptaciones realizadas, garantizan un equilibrio entre privacidad y usabilidad, permitiendo el uso seguro de los datos anonimizados para investigaciones futuras.

