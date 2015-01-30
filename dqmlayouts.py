from types import *
from re import *

class LayoutObj(object):
    """Base class for layout objects"""

    replacements_ = {}

    def __init__(self, name):
        self.name_ = name
    
    def expand(self, fil):
        pass

    def str(self, indentlevel=0):
        return ('    ' * indentlevel) + "-LayoutObj('" + self.name_ + "')\n"

    def clone(self, name=''):
        if name == '':
            name = self.name_
        lobj = LayoutObj(name)
        lobj.replacements_.update(self.replacements_)
        return lobj

    def _substitute(self, string):
        for ph in findall(r'\%\(([^\)]+)\)s', string):
            if ph not in self.replacements_:
                self.replacements_[ph] = '%(' + ph + ')s'
            
        return string % self.replacements_

class LayoutDir(LayoutObj):
    """Directory class"""

    pwd_ = ""

    def __init__(self, name, objs, addSerial = False):
        LayoutObj.__init__(self, name)
        # no cloning
        self.objs_ = objs
        # serial number of the elements in the directory
        self.serial_ = (0, 0)
        self.addSerial_ = addSerial

    def expand(self, fil):
        pwd = LayoutDir.pwd_
        if len(pwd):
            LayoutDir.pwd_ += "/" + self._substitute(self.name_)
        else:
            LayoutDir.pwd_ = self._substitute(self.name_)
            fil.write("def ecallayout(i, p, *rows): i[p] = DQMItem(layout=rows)\n\n")
            
        self.serial_ = (0, 0)
        for x in self.objs_:
            name = x.name_
            if x.addSerial_:
                serial = 0
                if issubclass(x.__class__, LayoutElem):
                    serial = self.serial_[0]
                    self.serial_ = (serial + 1, self.serial_[1])
                else:
                    serial = self.serial_[1]
                    self.serial_ = (self.serial_[0], serial + 1)
                    
                x.name_ = '%02d ' % serial + name

            x.expand(fil)
            x.name_ = name
        LayoutDir.pwd_ = pwd

    def str(self, indentlevel=0):
        result = ('    ' * indentlevel) + "-LayoutDir('" + self.name_ + "')\n"
        indentlevel += 1
        for x in self.objs_:
            result += x.str(indentlevel)
        return result

    def _copyObjs(self):
        newobjs = []
        for o in self.objs_:
            newobjs.append(o.clone())

        return newobjs

    def clone(self, name=''):
        if name == '':
            name = self.name_
        return LayoutDir(name, self._copyObjs(), self.addSerial_)

    def get(self, relPath):
        parts = relPath.split('/', 1)
        result = None
        for obj in self.objs_:
            if obj.name_ == parts[0]:
                if len(parts) == 2:
                    result = obj.get(parts[1])
                else:
                    result = obj

                if result:
                    break

        return result
    
    def remove(self, relPath):
        parts = relPath.split('/', 1)
        i = 0
        while i < len(self.objs_):
            obj = self.objs_[i]
            if obj.name_ == parts[0]:
                if len(parts) == 2:
                    obj.remove(parts[1])
                    if len(obj.objs_) == 0:
                        self.objs_.remove(obj)
                        i -= 1
                else:
                    self.objs_.remove(obj)
                    i -= 1

            i += 1

    def insert(self, name, obj):
        index = 0
        for x in self.objs_:
            if x.name_ == name :
                break
            index += 1
        if index == len(self.objs_):
            raise NameError(name + ' is not in the list of objects')
        
        if type(obj) is ListType:
            tmpList = self.objs_[0:index]
            tmpList = tmpList + obj
            self.objs_ = tmpList + self.objs_[index:len(self.objs_)]
        else:
            self.objs_.insert(index, obj)

    def append(self, obj):
        if type(obj) is ListType:
            self.objs_ = self.objs_ + obj
        else:
            self.objs_.append(obj)

class LayoutElem(LayoutObj):
    """Monitor element wrapper"""

    def __init__(self, name, layoutSpecs, addSerial = True):
        LayoutObj.__init__(self, name)
        # no copying
        self.layoutSpecs_ = layoutSpecs
        self.addSerial_ = addSerial

    def expand(self, fil):
        rows = []
        for row in self.layoutSpecs_:
            columns = []
            for column in row:
                if len(column) == 0:
                    columns.append(None)
                if len(column) == 1:
                    columns.append({'path' : self._substitute(column[0])})
                elif len(column) == 2:
                    columns.append({'path' : self._substitute(column[0]), 'description' : self._substitute(column[1])})
                else:
                    columns.append({'path' : self._substitute(column[0]), 'description' : self._substitute(column[1]), 'draw' : column[2]})

            rows.append(columns)
        
        fil.write("ecallayout(dqmitems, '" + LayoutDir.pwd_ + "/" + self._substitute(self.name_) + "'," + ','.join(map(str, rows)) + ")\n")

    def str(self, indentlevel=0):
        return ('    ' * indentlevel) + "-LayoutElem('" + self.name_ + "')\n"

    def _copySpecs(self):
        newspecs = []
        for row in self.layoutSpecs_:
            newspecs.append(list(row))
        return newspecs

    def clone(self, name=''):
        if name == '':
            name = self.name_
        return LayoutElem(name, self._copySpecs(), self.addSerial_)

class LayoutSet(LayoutObj):

    def __init__(self, name, repLists):
        LayoutObj.__init__(self, name)
        self.repLists_ = repLists

    def expand(self, fil):
        maxSize = 0
        paramSize = max(map(len, self.repLists_.values()))
        # aggregate the parameters for each entry
        for i in range(paramSize):
            for key, list in self.repLists_.items():
                replacement = ''
                if type(list) is StringType:
                    replacement = list
                elif i >= len(list):
                    replacement = list[len(list) - 1]
                else:
                    replacement = list[i]
                    
                LayoutObj.replacements_[key] = replacement
                
            template = self.generate()
            template.expand(fil)

        for key in self.repLists_.keys():
            LayoutObj.replacements_.pop(key)
            
    def generate(self):
        return LayoutObj(self.name_)

    def clone(self, name=''):
        if name == '':
            name = self.name_
        return LayoutSet(name, self.repLists_)

    def setReplacement(self, rep):
        self.repLists_ = rep

# LayoutSet must be the first inheritance
class LayoutDirSet(LayoutSet, LayoutDir):
    """Set of iteratively produced directories"""

    # objs: template of objects to be placed under each generated directory
    def __init__(self, name, objs, repLists, addSerial = False):
        LayoutSet.__init__(self, name, repLists)
        LayoutDir.__init__(self, name, objs, addSerial)

    def generate(self):
        return LayoutDir(self.name_, self.objs_, self.addSerial_)

    def str(self, indentlevel=0):
        result = ('    ' * indentlevel) + "-LayoutDirSet('" + self.name_ + "', " + str(self.repLists_) + ")\n"
        indentlevel += 1
        for x in self.objs_:
            result += x.str(indentlevel)
        return result

    def clone(self, name=''):
        if name == '':
            name = self.name_
        return LayoutDirSet(name, self._copyObjs(), self.repLists_, self.addSerial_)

# LayoutSet must be the first inheritance
class LayoutElemSet(LayoutSet, LayoutElem):
    """Set of iteratively produced elements"""

    def __init__(self, name, layoutSpecs, repLists, addSerial = True):
        LayoutSet.__init__(self, name, repLists)
        LayoutElem.__init__(self, name, layoutSpecs, addSerial)

    def generate(self):
        return LayoutElem(self.name_, self.layoutSpecs_, self.addSerial_)

    def str(self, indentlevel=0):
        return ('    ' * indentlevel) + "-LayoutElemSet('" + self.name_ + "', " + str(self.repLists_) + ")\n"

    def clone(self, name=''):
        if name == '':
            name = self.name_
        return LayoutElemSet(name, self._copySpecs(), self.repLists_, self.addSerial_)
