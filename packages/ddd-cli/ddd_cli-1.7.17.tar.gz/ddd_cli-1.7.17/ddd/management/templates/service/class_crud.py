class [[ entity_name.capitalize() ]]Service:
    """
    Servicio para manejar las operaciones CRUD relacionadas con [[ entity_name.lower() ]].

    Métodos disponibles:
        - create_[[ entity_name.lower() ]]: Crea una nueva instancia de [[ entity_name.lower() ]].
        - retrieve_[[ entity_name.lower() ]]: Recupera una instancia de [[ entity_name.lower() ]] por ID.
        - update_[[ entity_name.lower() ]]: Actualiza una instancia existente de [[ entity_name.lower() ]].
        - delete_[[ entity_name.lower() ]]: Elimina una instancia de [[ entity_name.lower() ]].
    """

    #Si necesitas mantener un estado de lista de entidades
    [[ entity_name.capitalize() ]]_list = []    


    def __init__(self, repository: [[ entity_name.capitalize() ]]Repository):
        """
        Inicializa el servicio con el repositorio correspondiente.

        :param repository: Repositorio que maneja la persistencia de [[ entity_name.lower() ]].
        """
        self.repository = repository    


    def list_[[ entity_name.lower() ]](self, filters: Optional[dict] = None) -> List[dict]:
        """
        Lista instancias de [[ entity_name.lower() ]].
    
        :param repository: Repositorio que maneja la persistencia de [[ entity_name.lower() ]].
        :return: Lista de la entidad.
        :raises ValueError: Si las reglas de negocio no se cumplen.
        """

        entity_list = self.repository.get_all(filters=filters)

        return [entity.to_dict() for entity in entity_list]      


    def count_all_[[ entity_name.lower() ]](self, filters: Optional[dict] = None) -> int:
        """
        Cuenta todas las instancias de [[ entity_name.lower() ]].

        :param filters: Filtros opcionales para la consulta.
        :return: Número total de instancias.
        """
        return self.repository.count_all(filters=filters)


    def create_[[ entity_name.lower() ]](self, external_id: Optional[int], data, adicionalData=None) -> dict:
        """
        Crea una nueva instancia de [[ entity_name.lower() ]].

        :param data: Diccionario o DTO con los datos necesarios para crear la instancia.
        :param adicionalData: Datos adicionales a incluir en la creación.
        :return: La entidad creada.
        :raises ValueError: Si las reglas de negocio no se cumplen.
        """
        # Validación de reglas de negocio (opcional)
        if repository.exists_by_field(field_name="attributeName", value=data['attributeName']):
            raise ValueError("An instance with this attributeName already exists")

        #crear y validar la entidad
        entity = [[ entity_name.capitalize() ]]Entity.from_dict(data)
        entity.validate()       

        # Guardar en el repositorio
        saved_entity = self.repository.create(entity=entity, external_id=external_id, adicionalData=adicionalData)

        return saved_entity.to_dict()


    def retrieve_[[ entity_name.lower() ]](self, entity_id: int) -> dict:
        """
        Recupera una instancia de [[ entity_name.lower() ]] por su ID.

        :param entity_id: ID de la instancia a recuperar.
        :return: La entidad recuperada.
        :raises ValueError: Si no se encuentra la instancia.
        """
        entity = self.repository.get_by_id(id=entity_id)
        if not entity:
            raise ValueError(f"No [[ entity_name.lower() ]] found with ID {entity_id}")

        return entity.to_dict()


    def update_[[ entity_name.lower() ]](self, entity_id: int, data, adicionalData=None) -> dict:
        """
        Actualiza una instancia existente de [[ entity_name.lower() ]].

        :param entity_id: ID de la instancia a actualizar.
        :param data: Diccionario o DTO con los datos a actualizar.
        :param adicionalData: Datos adicionales a incluir en la actualización.
        :return: La entidad actualizada.
        :raises ValueError: Si no se encuentra la instancia o las reglas de negocio no se cumplen.
        """
        # Recuperar la entidad
        entity = self.repository.get_by_id(id=entity_id)
        if not entity:
            raise ValueError(f"No [[ entity_name.lower() ]] found with ID {entity_id}")

        # actualizar la instancia y validar
        entity.update(data)     
        entity.validate()   

        # Guardar en el repositorio
        updated_entity = self.repository.save(entity=entity, adicionalData=adicionalData)
        
        return updated_entity.to_dict()


    def delete_[[ entity_name.lower() ]](self, entity_id: int) -> bool:
        """
        Elimina una instancia de [[ entity_name.lower() ]].

        :param entity_id: ID de la instancia a eliminar.
        :return: True/False (depende del exito de la operacion)
        :raises ValueError: Si no se encuentra la instancia.
        """
        # Recuperar la entidad
        entity = self.repository.get_by_id(id=entity_id)
        if not entity:
            raise ValueError(f"No [[ entity_name.lower() ]] found with ID {entity_id}")

        # Eliminación en el repositorio
        self.repository.delete(id=entity_id)

        return True
