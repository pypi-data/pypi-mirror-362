from repository_miner.git import *
from pytest import fixture,mark,param
from pathlib import Path
from repository_miner import execute_command,cmd_builder
main_path=Path.cwd()
@fixture
def git():
    try:
        return Git(main_path.as_posix())
    except GitNotFoundException as e:
        return None
    
@fixture
def version_checker():
    try:
        Git(main_path.as_posix())
        return True
    except GitNotFoundException as e:
        print(e)
        version=execute_command(cmd_builder("",main_path.as_posix(),"--version"))
        version=version.split(".",3)
        version[0]=version[0].rsplit(" ",1)[-1]
        version=dict(major=version[0],minor=version[1],path=version[2])
        if int(version["major"])==2 and int(version["minor"])<39 or int(version["major"])<2:
            return False
        else:
            return True


@mark.parametrize("args,expected",[
    param("rev_parse",execute_command(cmd_builder("rev-parse",main_path.as_posix(),"HEAD")).strip()),
    param("rev_pars",None,marks=mark.xfail),
    param("",None,marks=mark.xfail),
    param(None,None,marks=mark.xfail),
])
def test_any_cmd(git,version_checker,args,expected):
    if not version_checker:
        assert expected != None
        return
    assert git.__getattr__(args)(["HEAD"])==expected
    # print(res)

@mark.parametrize("args,expected",[
    param(["-5",r"--pretty='format:%ad'","--numstat"],execute_command(cmd_builder("log",main_path.as_posix(),r"--pretty='format:%ad'","--numstat","-5"))),
    param(["-5"],execute_command(cmd_builder("log",main_path.as_posix(),"-5"))),
    param("-asda",None,marks=mark.xfail),
])
def test_any_arg(git,version_checker,args,expected):
    if not version_checker:
        assert expected != None
        return
    assert git.log(*args)==expected
    # print(res.split('\n'))
#TODO need to complete test cases as needed
def test_git_grep(git,version_checker):
    if not version_checker:
        assert True
        return
    print(git.grep(["-E","-n","-o","-I",f'\"[^a-zA-Z0-9_]+\\s*({"|".join(["TODO","FIXME"])}).+\"']))

