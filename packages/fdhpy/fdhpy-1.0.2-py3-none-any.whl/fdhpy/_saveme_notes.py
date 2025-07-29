# How to handle model-specific kwargs in the module & cli

    def __init__(self, **kwargs):
        kwargs.setdefault("metric", "principal")
        kwargs.setdefault("version", "d/ad")
        kwargs.setdefault("style", "reverse")

        self.bar = kwargs.pop("bar", 9) #<-----------------
        super().__init__(**kwargs)


    def displ_avg(self) -> Optional[float]:
        print(self.bar) #<----------------- checker
        return self._normalized_calcs._compute_avg_displ()


    @staticmethod
    def add_arguments(parser):
        # Add arguments specific to ChildC
        parser.add_argument("--bar", default=9, type=int, help="An argument specific to ChildC")

    @staticmethod
    def main():
        cli_runner(MossRoss2011, MossRoss2011.add_arguments)
        
        
""" Notes
Why use pop here?
    Avoid passing unwanted keys to the parent class: 
        The parent class's __init__ method may not expect the "use_girs" key, and you don't want it 
        to be included in the kwargs passed to super().__init__(**kwargs). By using pop, you remove 
        the key from kwargs before passing the remaining dictionary to the parent class.
    Control over key-value handling: 
        The "use_girs" value is handled separately, possibly because it needs to be stored in an 
        instance variable (self.use_girs), while other arguments are passed directly to the parent 
        class.
"""
