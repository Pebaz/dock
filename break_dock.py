import dock


@dock
class ThisIsFine:
    @dock
    def okay(self):
        ...
    
    def ignored(self):
        ...

    @dock
    def fine(self):
        ...

    @dock
    class StillFine:
        @dock
        def broken(self):
            ...
    
    @dock
    def broken(self):
        ...