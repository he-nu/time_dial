# Module for defining features of the ascii art and timeline

class Art:
    def __init__(self, art:str) -> None:
        self.art = art
        self.H = self.height(art)
        self.W = self.width(art)
        self.lines:list = art.splitlines()[1:]

    def height(self, art:str) -> int:
        return art.count("\n") - 1

    def width(self, art:str) -> int:
        return max([len(line) for line in art.splitlines()]) # Longest line
        
    def show(self):
        print(self.art)
    

class TimeLine:
    # numbers for the horisontal
    horisontal = "____________________________________________________________________________"
    overline =   "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾"

    def __init__(self) -> None:
        self.numline =  f"{' '*6} {self.make_nums()}"
        self.timeline = f"{self.horisontal}\n{self.numline}"
    def make_nums(self):
        pad = 4
        _space = " " * pad 
        reduced_space = " " * (pad - 1)
        clock_nums = [str(i) for i in range(6, 13)]
        one_to_six = [str(i) for i in range(1, 7)]
        for i in one_to_six:
            clock_nums.append(i)
        for i in range(1, len(clock_nums)):
            if len(clock_nums[i]) == 2:
                clock_nums[i] = reduced_space + clock_nums[i]
            else:
                clock_nums[i] = f"{_space}{clock_nums[i]}"


        return "".join(clock_nums)

if __name__ == "__main__":

    clockface = TimeLine()
    print(clockface.timeline)

