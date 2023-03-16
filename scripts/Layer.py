import layer_sorting as sorting
import obplib as obp
import Shape
import file_import

class Layer:
    shapes = [] #array of Shape objects
    shapes_to_export = [] #array with sorted shapes to export
    sorting_strategy = "shapes_first" #defines the order in which the shapes are manufactured
    sorting_settings = dict() #appends settings to the sorting algorithm

    def create_obp_elements(self):
        self.sort_layers()
        obp_elements = []
        for shape in self.shapes_to_export:
            shape.generate_melt_strategy()
            shape.generate_obp_elements()
            obp_elements = obp_elements + shape.obp_elements
        return obp_elements

    def export_obp(self,path):
        obp_elements = self.create_obp_elements()
        obp.write_obp(obp_elements,path)
    
    def export_obpj(self,path):
        obp_elements = self.create_obp_elements()
        obp.write_obpj(obp_elements,path)

    def set_manufacturing_settings(self,manufacturing_settings):
        if not type(manufacturing_settings) is list:
            manufacturing_settings = [manufacturing_settings]*len(self.shapes)
        elif not len(manufacturing_settings) == len(self.shapes):
            manufacturing_settings = [manufacturing_settings[0]]*len(self.shapes)
        for i in range(len(self.shapes)):
            self.shapes[i].manufacturing_settings = manufacturing_settings[i]
    
    def set_melt_strategies(self,melt_strategies):
        if not type(melt_strategies) is list:
            melt_strategies = [melt_strategies]*len(self.shapes)
        elif not len(melt_strategies) == len(self.shapes):
            melt_strategies = [melt_strategies[0]]*len(self.shapes)
        for i in range(len(self.shapes)):
            self.shapes[i].melt_strategy = melt_strategies[i]
    
    def set_nmb_of_scans(self, nmb_of_scans):
        if not type(nmb_of_scans) is list:
            nmb_of_scans = [nmb_of_scans]*len(self.shapes)
        elif not len(nmb_of_scans) == len(self.shapes):
            nmb_of_scans = [nmb_of_scans[0]]*len(self.shapes)
        for i in range(len(self.shapes)):
            self.shapes[i].nmb_of_scans = nmb_of_scans[i]

    def set_shapes(self, spacing, size=300, angle=0):
        if not type(spacing) is list:
            spacing = [spacing]*len(self.shapes)
        elif not len(spacing) == len(self.shapes):
            spacing = [spacing[0]]*len(self.shapes)
        if not type(size) is list:
            size = [size]*len(self.shapes)
        elif not len(size) == len(self.shapes):
            size = [size[0]]*len(self.shapes)
        if not type(angle) is list:
            angle = [angle]*len(self.shapes)
        elif not len(angle) == len(self.shapes):
            angle = [angle[0]]*len(self.shapes)

        for i in range(len(self.shapes)):
            self.shapes[i].generate_matrixes(spacing[i], size[i], angle[i])
            self.shapes[i].check_keep_matrix()
            import numpy as np
            x = self.shapes[i].keep_matrix
            nonZero = np.count_nonzero(x == 2)
            #print(nonZero)

    def sort_layers(self, strategy=None,settings=None):
        if strategy is None:
            strategy = self.sorting_strategy
        if settings is None:
            settings = self.sorting_settings
        self.shapes_to_export = sorting.sort(self.shapes,strategy=strategy,settings=settings)

    def import_svg_layer(self, path):
        matplot_paths = file_import.import_svg_layer(path)
        for path in matplot_paths:
            new_shape = Shape.Shape()
            new_shape.paths = path
            self.shapes.append(new_shape)




        

