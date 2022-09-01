import os

class CartesianPoint:
    def __init__(self, x = 0, y = 0, z = 0, a = 0, b = 0, c = 0,
                       e1 = 0, e2 = 0, e3 = 0, e4 = 0):
        self.x = x; self.y = y; self.z = z; 
        self.a = a; self.b = b; self.c = c;
        self.e1 = e1; self.e2 = e2;
        self.e3 = e3; self.e4 = e4;

class JointPoint:
    def __init__(self, a1 = 0, a2 = 0, a3 = 0, a4 = 0, a5 = 0, a6 = 0,
                       e1 = 0, e2 = 0, e3 = 0, e4 = 0):
        self.a1 = a1; self.a2 = a2; self.a3 = a3; 
        self.a4 = a4; self.a5 = a5; self.a6 = a6;
        self.e1 = e1; self.e2 = e2;
        self.e3 = e3; self.e4 = e4;

class Position:
    def __init__(self, x = 0, y = 0, z = 0, a = 0, b = 0, c = 0):
        self.x = x; self.y = y; self.z = z; 
        self.a = a; self.b = b; self.c = c;

class SrcGenerator:    
    
    def __init__ (self, fName, loc = './', ADV = 3, homePos = JointPoint(a2 = -90, a3 = 90, a5 = -90)):
        self.fName = fName;
        self.src = open(os.path.join(loc, fName +'.src'), 'w');
        self.src.write('DEF ' + fName.upper() + '()\n');
        #this is a copy of what kukaPRC outputs.
        self.src.write(';FOLD INI\n' +
                       ';FOLD BASISTECH INI\n' +
                       'GLOBAL INTERRUPT DECL 3 WHEN $STOPMESS==TRUE DO IR_STOPM ( )\n' +
                       'INTERRUPT ON 3\n' +
                       'BAS (#INITMOV,0 )\n' +
                       ';ENDFOLD (BASISTECH INI)\n' +
                       ';ENDFOLD (INI)\n'+
                       '\n' +
                       ';FOLD STARTPOSITION - BASE IS 0, TOOL IS 3, SPEED IS 100%, POSITION IS externally defined -> se generating script\n' +
                       '$BWDSTART = FALSE\n' +
                       'PDAT_ACT = {VEL 100,ACC 100,APO_DIST 50}\n' + #CATCH APO_DIST somewhere!!!!
                       'FDAT_ACT = {TOOL_NO 0,BASE_NO 0,IPO_FRAME #BASE}\n' + 
                       'BAS (#PTP_PARAMS,100)\n'
        );
        self.src.write('PTP {A1 %f, A2 %f, A3 %f, A4 %f, A5 %f, A6 %f, E1 %f, E2 %f, E3 %f, E4 %f}\n;ENDFOLD\n\n' 
                       % (homePos.a1, homePos.a2, homePos.a3, homePos.a4, homePos.a5, homePos.a6, homePos.e1, homePos.e2, homePos.e3, homePos.e4)
        );
        
    
    def linMotion(self, p = CartesianPoint()):
        self.src.write('LIN {X %f, Y %f, Z %f, A %f, B %f, C %f, E1 %f, E2 %f, E3 %f, E4 %f} C_DIS\n' 
                        % (p.x, p.y, p.z, p.a, p.b, p.c, p.e1, p.e2, p.e3, p.e4));
    
    def ptpMotion(selt, p = CartesianPoint()):
        self.src.write('PTP {X %f, Y %f, Z %f, A %f, B %f, C %f, E1 %f, E2 %f, E3 %f, E4 %f} C_DIS\n' 
                        % (p.x, p.y, p.z, p.a, p.b, p.c, p.e1, p.e2, p.e3, p.e4));
    
    def setBaseByPosition(self, p = Position()):
        self.src.write('$BASE = {X %f, Y %f, Z %f, A %f, B %f, C %f}\n'
                        % (p.x, p.y, p.z, p.a, p.b, p.c));

    def setToolByPosition(self, p = Position()):
        self.src.write('$TOOL = {X %f, Y %f, Z %f, A %f, B %f, C %f}\n'
                        % (p.x, p.y, p.z, p.a, p.b, p.c));
    
    def setBaseByID(self, ID = 0):
        self.src.write('BAS(#BASE, ' + str(ID) + ')\n');
    
    def setToolByID(self, ID = 0):
        self.src.write('BAS(#TOOL, ' + str(ID) + ')\n');
    
    def delay(self, t=0):#SECONDS!
        self.src.write('WAIT SEC %f\n' % (t));
    
    def setDOut(self, ID = 0, value = 'FALSE'):
        self.src.write('$OUT[' + str(ID) + '] = ' + value + '\n');
    
    def setAOut(self, ID = 0, value = 0.0):
        self.src.write('$ANOUT[' + str(ID) + '] = ' + str(value) + '\n');
    
    #these should provide some freedom for writing custom KRL code into your program
    def setBAS(self, varName = '', varValue = 0):
        self.src.write('BAS(' + varName + ', ' + str(varValue) + ')\n');
    
    def writeFreeKRL(self, content = ''):
        self.src.write(content);        
    
    def fuck(self):
        pass;
    
    def close(self):
        self.src.write('END\n');
        self.src.close();