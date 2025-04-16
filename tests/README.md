# Tests de la Aplicación de Notas

## Estructura de los Tests

Los tests siguen la misma estructura que la aplicación, divididos en:

- **Unit Tests**: Prueban el comportamiento de los componentes de forma aislada
- **Integration Tests**: Prueban la integración entre componentes
- **E2E Tests**: Prueban la aplicación completa desde la perspectiva del usuario

## Enfoque de Testing

Utilizamos **pytest** como framework de testing, con fixtures para proporcionar entornos de test consistentes.

### Fixtures

Las fixtures se organizan en archivos `conftest.py` en diferentes niveles para proporcionar un alcance adecuado:

- `tests/conftest.py`: Fixtures globales para todos los tests
- `tests/unit/conftest.py`: Fixtures para tests unitarios
- `tests/unit/notes/conftest.py`: Fixtures específicas para los tests de notas
- `tests/unit/notes/application/conftest.py`: Fixtures para los servicios de aplicación

### Patrones de Testing

En lugar de utilizar el patrón **Mother Object** para crear objetos de prueba, ahora utilizamos:

1. **Factory Fixtures**: Para crear objetos de test personalizables
2. **Fixtures de Servicios**: Que proporcionan instancias de servicios para los tests
3. **Fixtures de Datos**: Que proporcionan datos de ejemplo

### Ejemplo de Uso

```python
# Test usando fixtures
@pytest.mark.asyncio
async def test_create_note(create_note_service, sample_note, note_repository):
    # Arrange
    title_value = sample_note.title.value
    content_value = sample_note.content.value
    
    # Act
    created_note = await create_note_service(title_value, content_value)
    
    # Assert
    assert created_note.title.value == title_value
    assert created_note.content.value == content_value
    note_repository.save.assert_called_once()
```

## Beneficios de este Enfoque

1. **Mayor reutilización de código** - Las fixtures se comparten entre tests
2. **Tests más legibles** - Enfoque en el comportamiento, no en la configuración
3. **Más mantenible** - Cambios en las fixtures se propagan a todos los tests
4. **Fácil parametrización** - Pruebas con diferentes conjuntos de datos 