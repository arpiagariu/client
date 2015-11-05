""" run with

python setup.py install; nosetests -v --nocapture  tests/test_group.py:Test_group.test_001

nosetests -v --nocapture tests/test_group.py

or

nosetests -v tests/test_group.py

"""
import os

from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import HEADING
from cloudmesh_base.util import banner

from cloudmesh_client.cloud.group import Group
from cloudmesh_client.cloud.default import Default

def run(command):
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return result

class Test_group:

    def sh(self, command):
        banner(command)
        run(command)

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        """testing cm group add groupA --cloud=juno --id=test-001 --type=vm"""
        HEADING()

        c = "cm group add groupA --cloud=juno --id=test-001 --type=vm"
        self.sh(c)


        id = str(Group.get(name="groupA", cloud="juno"))
        print id
        assert "test-001" in id
        return

    def test_002(self):
        """testing cm group add groupA --cloud=juno --id=test-002 --type=vm"""
        HEADING()
        self.sh("cm group add groupA --cloud=juno --id=test-002 --type=vm")
        group = Group.get(name="groupA", cloud="juno")
        assert group["cloud"] == "juno"
        assert group["name"] == "groupA"
        assert group["type"] == "vm"
        #
        # TODO: there seems to be a bug here, what is id?
        # id is internal and should not be set buy this.
        assert group["value"] == "test-001,test-002"
        return

    def test_003(self):
        """testing cm group copy groupA groupB"""
        HEADING()
        banner("cm group copy groupA groupB")

        result = run("cm group copy groupA groupB")
        assert "[groupB]" in result

        return

    def test_004(self):
        """testing cm group merge groupA groupB groupC"""
        HEADING()
        banner("cm group merge groupA groupB groupC")

        result = run("cm group merge groupA groupB groupC")
        assert "successful!" in result
        return

    def test_005(self):
        """testing cm group list --cloud=juno groupA"""
        HEADING()
        banner("cm group list --cloud=juno groupA")

        result = run("cm group list --cloud=juno groupA")
        assert "groupA" in result
        return

    def test_006(self):
        """testing cm group list --cloud=juno --format json groupA"""
        HEADING()
        banner("cm group list --cloud=juno --format=json groupA")

        result = run("cm group list --cloud=juno  --format=json groupA")
        assert "groupA" in result
        return

    def test_007(self):
        """testing cm group list --cloud=juno --format table"""
        HEADING()
        banner("cm group list --cloud=juno --format=table")

        result = run("cm group list --cloud=juno --format=table")
        assert "groupA" in result
        return

    def test_008(self):
        """testing cm group add --name=groupX --id albert-00x [WITH DEFAULT CLOUD=juno, TYPE=VM]"""
        HEADING()
        banner("cm group add --name=groupX --id=albert-00x")

        result1 = run("cm default cloud=juno")
        assert "juno" in result1
        assert "cloud" in result1
        assert "ok" in result1

        result1 = run("cm default type=vm")
        assert "ok." in result1

        result2 = run("cm group add groupX --id=albert-00x")
        assert "albert-00x" in result2

        result3 = run("cm group list --cloud=juno groupX")
        assert "juno" in result3
        assert "vm" in result3

        return

    def test_009(self):
        """testing cm group remove --cloud=juno --name=groupA --id=test-002"""
        HEADING()
        banner("cm group remove --cloud=juno --name=groupA --id=test-002")

        result1 = run("cm group remove --cloud=juno --name=groupA --id="
                      "test-002")
        print(result1)
        assert "Successfully removed ID" in result1

        result2 = run("cm group list groupA")
        assert "test-002" not in result2

        return

    def test_010(self):
        """testing cm group delete groupA --cloud=juno"""
        HEADING()
        """
        banner("cm group delete groupA --cloud=juno")
        result = run("cm group delete groupA --cloud=juno")
        print(result)
        assert "ok." in result
        """

        banner("cm group delete groupB --cloud=juno")
        result = run("cm group delete groupB --cloud=juno")
        assert "ok." in result

        banner("cm group delete groupC --cloud=juno")
        result = run("cm group delete groupC --cloud=juno")
        assert "ok." in result

        banner("cm group delete groupX")
        result = run("cm group delete groupX")
        assert "ok." in result

        # Cleanup defaults
        run("cm default delete cloud")
        run("cm default delete type")

        return

