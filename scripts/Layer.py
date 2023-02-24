import layer_sorting as sorting

class Layer:
    shapes = [] #array of Shape objects
    shapes_to_export = [] #array with sorted shapes to export

    def sort_layers(self, strategy="shapes_first",settings=dict()):
        self.shapes_to_export = sorting.sort(self.shapes,strategy=strategy,settings=settings)

        
        

