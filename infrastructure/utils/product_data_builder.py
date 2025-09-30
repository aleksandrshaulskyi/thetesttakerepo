class ProductDataBuilder:

    def build(self, item: tuple, file_name: str) -> dict:
        try:
            query = item[0]
            quantity = item[1]
        except IndexError:
            pass

        return {
            'query': query,
            'quantity': quantity,
            'file_name': file_name,
        }
    
product_data_builder = ProductDataBuilder()
