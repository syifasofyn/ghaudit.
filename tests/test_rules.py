from ghaudit.rules import check_unpinned_actions       # ambil fungsi yang mau dites


def test_tag_dianggap_tidak_aman():                    # awalan "test_" = dikenali pytest
    wf = {"jobs": {"build": {"steps": [{"uses": "actions/checkout@v4"}]}}}  # workflow palsu pakai tag
    assert len(check_unpinned_actions("ci.yml", wf)) == 1   # harus ada tepat 1 temuan


def test_sha_dianggap_aman():                          # test kasus aman
    wf = {"jobs": {"build": {"steps": [{"uses": "actions/checkout@" + "a" * 40}]}}}  # "a" * 40 = 40 huruf a (SHA palsu)
    assert check_unpinned_actions("ci.yml", wf) == []  # harus tidak ada temuan