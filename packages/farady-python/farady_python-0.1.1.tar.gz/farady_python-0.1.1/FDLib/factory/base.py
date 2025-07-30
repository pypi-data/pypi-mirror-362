class FDBase:
    metalLayers = []
    Parameters = {}
    ParameterOrder = []
    chosen_parameters = {}
    pins = []

    def check_param(self):
        raise NotImplementedError()

    def reload(self):
        raise NotImplementedError()

    def show(self):
        raise NotImplementedError()

    def run(self):
        [setattr(self, k, v) for k, v in self.Parameters.items()]
        self.reload()
        self.show()
