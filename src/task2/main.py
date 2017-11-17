import classifier as c


__author__ = "Keoagile Dinake"


def main():
    print(c.LIME + "Task 2: Modelling")
    print("=" * 40 + c.RESET)
    detective = c.Classifier()
    detective.use_dataset("creditcard.csv")
    detective.prepare_dataset()
    detective.fit()
    detective.predict_and_report()
    print(c.LIME + "=" * 40)
    print("Analysis complete\nReport is located at: reports/CreditCard_Report.pdf" + c.RESET)


if __name__ == '__main__':
    main()
