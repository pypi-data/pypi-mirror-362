import o7util.pandas

import o7pdf.report_security_hub_standard as report


def test_basic():
    dfs = o7util.pandas.dfs_from_excel("tests/sechub-data.xlsx")

    obj = report.ReportSecurityHubStandard(filename="cache/security_hub_standard.pdf")
    obj.generate(dfs=dfs, standard_arn="standards/cis-aws-foundations-benchmark/v/3.0.0")
    obj.save()


def test_o7_org():
    dfs = o7util.pandas.dfs_from_excel("tests/sechub-data-o7-20241021.xlsx")

    obj = report.ReportSecurityHubStandard(filename="cache/security_hub_standard_o7_org.pdf")
    obj.generate(dfs=dfs, standard_arn="standards/cis-aws-foundations-benchmark/v/3.0.0")
    obj.save()
