from skimage.measure import shannon_entropy


## 1um 64*64*64 NISSEL VISOR mouse brain, foreground thres: shannon_entropy > = 1.8
## 4um 64*64*64 NISSEL VISOR rm009 brain, foreground thres: shannon_entropy > = 2.7
def entropy_filter(thres=1.8):
    def _filter(img):
        entropy=shannon_entropy(img)
        return entropy>thres
    return _filter