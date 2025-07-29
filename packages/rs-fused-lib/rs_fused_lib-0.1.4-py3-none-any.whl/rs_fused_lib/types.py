class Bounds:
    """
    表示地理空间的边界框 (minx, miny, maxx, maxy)
    支持元组、列表初始化，支持属性访问和常用方法。
    """
    __module__ = "rs_fused_lib.types"
    def __init__(self, bounds):
        if isinstance(bounds, Bounds):
            self.minx, self.miny, self.maxx, self.maxy = bounds.minx, bounds.miny, bounds.maxx, bounds.maxy
        elif isinstance(bounds, (list, tuple)) and len(bounds) == 4:
            self.minx, self.miny, self.maxx, self.maxy = map(float, bounds)
        else:
            raise ValueError("Bounds 需要4个元素 (minx, miny, maxx, maxy)")

    def __iter__(self):
        return iter((self.minx, self.miny, self.maxx, self.maxy))

    def __getitem__(self, idx):
        return (self.minx, self.miny, self.maxx, self.maxy)[idx]

    def __repr__(self):
        return f"Bounds({self.minx}, {self.miny}, {self.maxx}, {self.maxy})"

    def to_tuple(self):
        return (self.minx, self.miny, self.maxx, self.maxy)

    def width(self):
        return self.maxx - self.minx

    def height(self):
        return self.maxy - self.miny

    def area(self):
        return self.width() * self.height()

    def is_valid(self):
        return self.maxx > self.minx and self.maxy > self.miny 