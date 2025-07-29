#!/usr/bin/env python
"""
killMS, a package for calibration in radio interferometry.
Copyright (C) 2013-2017  Cyril Tasse, l'Observatoire de Paris,
SKA South Africa, Rhodes University

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections
import optparse as OptParse
from . import PrintOptParse
from . import ReadCFG

from . import ClassPrint
from killMS.Other import ModColor
from killMS.Other.logo import report_version
#global Parset
#Parset=ReadCFG.Parset("/media/tasse/data/DDFacet/Parset/DefaultParset.cfg")
#D=Parset.DicoPars 

class MyOptParse():
    def __init__(self,usage='Usage: %prog --ms=somename.MS <options>',version=report_version(),
                 description="""Questions and suggestions: cyril.tasse@obspm.fr""",
                 DefaultDict=None):
        self.opt = OptParse.OptionParser(usage=usage,version=version,description=description)
        self.DefaultDict=DefaultDict
        self.CurrentGroup=None
        self.DicoGroupDesc=collections.OrderedDict()
        # remember parameter types so we can generate a schema, if needed
        self.parameter_types = collections.OrderedDict()

    def OptionGroup(self,Name,key=None):
        if self.CurrentGroup!=None:
            self.Finalise()
        self.CurrentGroup = OptParse.OptionGroup(self.opt, Name)
        self.CurrentGroupKey=key
        self.DicoGroupDesc[key]=Name


    def GiveOptionObject(self):
        DC=self.GiveDicoConfig()
        class Object(object):
            pass

        options=Object()
        for Field in DC.keys():
            D=DC[Field]
            for key in D.keys():
                setattr(options, key, D[key])
        return options

    def add_option(self,Name='Mode',help='Default %default',type="str",default=None):
        if default==None:
            default=self.DefaultDict[self.CurrentGroupKey][Name]
        
        self.CurrentGroup.add_option('--%s'%Name,help=help,type=type,default=default,dest=self.GiveKeyDest(self.CurrentGroupKey,Name))
        self.parameter_types[Name] = type

    def GiveKeyDest(self,GroupKey,Name):
        return "_".join([GroupKey,Name])

    def GiveKeysOut(self,KeyDest):
        return KeyDest.split("_")

    def Finalise(self):
        self.opt.add_option_group(self.CurrentGroup)

    def ReadInput(self):
        self.options, self.arguments = self.opt.parse_args()
        self.GiveDicoConfig()
        self.DicoConfig=self.DefaultDict
        
    def GiveDicoConfig(self):
        DicoDest=vars(self.options)
        for key in DicoDest.keys():
            GroupName,Name=self.GiveKeysOut(key)
            val=DicoDest[key]
            if type(val)==str:
                val=ReadCFG.FormatValue(val)
            self.DefaultDict[GroupName][Name]=val

        return self.DefaultDict

    def ToParset(self,ParsetName):
        Dico=self.GiveDicoConfig()
        f=open(ParsetName,"w")
        for MainKey in Dico.keys():
            f.write('[%s]\n'%MainKey)
            D=Dico[MainKey]
            for SubKey in D.keys():
                f.write('%s = %s \n'%(SubKey,str(D[SubKey])))
            f.write('\n')
        f.close()

    def Print(self,RejectGroup=[]):
        P=ClassPrint.ClassPrint(HW=50)
        print(ModColor.Str(" Selected Options:"))
    
        for Group,V in self.DefaultDict.items():
            Skip=False
            for Name in RejectGroup:
                if Name in Group:
                    Skip=True
            if Skip: continue
            try:
                GroupTitle=self.DicoGroupDesc[Group]
            except:
                GroupTitle=Group
            print(ModColor.Str(GroupTitle,col="green"))
    
            option_list=self.DefaultDict[Group]
            for oname in option_list:
                V=self.DefaultDict[Group][oname]
                
                if True:#V!="":
                    if V=="": V="''"
                    P.Print(oname,V)
            print()



def test():
    OP=MyOptParse()
    
    OP.OptionGroup("* Data","VisData")
    OP.add_option('MSName',help='Input MS')
    OP.add_option('ColName')
    OP.Finalise()
    OP.ReadInput()
    Dico=OP.GiveDicoConfig()
    OP.Print()
    
    return OP.DefaultDict
    

if __name__=="__main__":
    test()

