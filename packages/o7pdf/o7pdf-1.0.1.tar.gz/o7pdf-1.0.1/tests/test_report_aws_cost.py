import o7util.pandas

import o7pdf.report_aws_cost as report


def test_basic():
    dfs = o7util.pandas.dfs_from_excel("tests/aws-cost-data.xlsx")
    obj = report.ReportAwsCost(filename="cache/aws_cost.pdf")
    obj.generate(dfs=dfs)
    obj.save()


def test_forecast():
    dfs = o7util.pandas.dfs_from_excel("tests/aws-cost-data-20250219.xlsx")
    obj = report.ReportAwsCost(filename="cache/aws_cost_forecast.pdf", forecast=True)
    obj.generate(dfs=dfs)
    obj.save()


if __name__ == "__main__":
    # test_basic()
    test_forecast()
