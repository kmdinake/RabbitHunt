__author__ = "Keoagile Dinake"
import cleaner as c


def main():
    print(c.LIME + "Task 1: Exploratory Data Analysis")
    print("="*40 + c.RESET)
    scrubber = c.Cleaner()
    scrubber.use_dataset("HR_comma_sep.csv")
    scrubber.scrub_dataset()
    scrubber.report("Scrubber_Report.txt")
    print(c.LIME + "="*40)
    print("Analysis complete" + c.RESET)


if __name__ == "__main__":
    main()