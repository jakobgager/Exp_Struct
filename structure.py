#! /usr/bin/env python

from math import sqrt, ceil

def fbd_template(tempdict):
    return """
    # Crosssection
    Pnt P1 -{l2} -{w2} -{h2}
    Pnt P2 -{l2} -{w2} {PC1z}
    Pnt P3 -{l2} -{PC1y} {h2} 
    Pnt PC1 -{l2} -{PC1y} {PC1z}
    Pnt P4  -{l2} 0  {h2}
    Line L1 P1 P2 {L1div}
    Line L2 P2 P3 PC1 {L2div}
    Line L3 P3 P4 {L3div}
    Seta CS1 l L1 L2 L3
    
    # Flaeche 1
    Seto Struct1
    Swep CS1 CS2 tra {la} 0 0 {ladiv}
    Setc Struct1
    
    # Flaeche 2
    Seto Struct2
    Swep CS2 CS3 tra {lcl} 0 0 {lcldiv}
    Setc Struct2
    
    # Flaeche 3
    Seto Struct3
    Pnt P5 0 -{w2} {P5z}
    Pnt PC2 0 -{w2} {PC2z}
    Seta CS3a l L00B L00A
    Swep CS3a CS4a tra {wc} 0 0 {wcdiv}
    Line L4 D006 P5 PC2 {wcdiv}
    Line L5 P5 D00B {L5div}
    Surf S1 L4 L5 L00J L009
    Setc Struct3
    
    Seta struct_all se Struct1 Struct2 Struct3
    
    # Load block
    Seto block1
    Pnt P8 -{l2} 0 -{h2}
    Pnt P11 -{l2} 0 {PC1z}
    Line L6 P1 P8 {L6div}
    Line L7 P8 P11 {L1div}
    Line L9 P11 P4 {L2div}
    Line L11 P2 P11 {L6div}
    Surf S2 L1 L11 L7 L6
    Surf S3 L11 L2 L3 L9
    Swep block1 temp tra {la} 0 0 {ladiv}
    Setc block1
    
    # Load block 2
    Seto block2
    Pnt P9 -{P9x} 0 {h2}
    Pnt P10 -{P9x} 0 {P10z}
    Line L8 P9 P10 2
    Swep block2 temp1 tra 0 -{w2} 0 {L6div}
    Swep block2 temp2 tra {wd} 0 0 {wddiv}
    Setc block2
    
    # Element types
    Elty struct_all qu8
    Elty block1 he20
    Elty block2 he20
    
    Mesh struct_all
    Mesh block1
    Merg n all
    Mesh block2
    
    Seta Sym_X l L00I L00H L5
    Seta Sym_Y l L00G L00M 
    Seta Sym_Y s A00F A00G A00K

    Comp Sym_X d
    Comp Sym_Y d
    
    # Change mesh order to quadratic
    #Mids all gen

    plot e all
    view elem
    plus e block1 m
    plus e block2 b
    plus e struct_all g

    # write mesh
    send struct_all abq
    send block1 abq
    send block2 abq
    send Sym_X abq names
    send Sym_Y abq names
    """.format(**tempdict)

def comp_variables():
    # compute helpers
    globs = {}
    execfile('dimensions.py', globs)

    # crosssection 1
    st = globs['structure']
    st['l2'] = st['l']/2.
    st['w2'] = st['w']/2.
    st['h2'] = st['h']/2.
    st['lf2'] = st['lf']/2.
    st['PC1z'] = st['h2'] - st['r']
    st['PC1y'] = st['w2'] - st['r']
    
    # cut out
    st['wc'] = sqrt(st['rc']**2 - st['lc']**2)
    st['lcl'] = st['l2'] - st['la'] - st['wc']
    st['PC2z'] = -st['h2'] - st['lc']
    st['P5z'] = st['PC2z'] + st['rc']
    
    # load block 2
    st['P9x'] = st['lf2'] + st['wd']/2.
    st['P10z'] = st['h2'] + st['td']

    # linedivisions
    st['L1div'] = evenint((st['h']-st['r'])/st['es'])
    st['L2div'] = evenint(ceil((st['r']*1.5)/st['es']))
    st['L3div'] = evenint((st['w2']-st['r'])/st['es'])
    st['ladiv'] = evenint(st['la']/st['es'])
    st['lcldiv'] = evenint(st['lcl']/st['es'])
    st['wcdiv'] = evenint(st['wc']/st['es'])
    st['L5div'] = evenint((st['h2'] - st['P5z'])/st['es'])
    st['L6div'] = evenint(st['w2']/st['es'])
    st['L7div'] = evenint(st['h']/st['es'])
    st['wddiv'] = evenint(st['wd']/st['es'])
    st['tddiv'] = evenint(ceil(st['td']/st['es']))

    return st

def evenint(x):
    x = int(x)
    if x%2 == 0: 
        return x
    else:
        return x+1


def main():
    struct = comp_variables()
    fbd_data = fbd_template(struct)

    with open('exp_struct.fbd','w') as fil:
        fil.writelines(fbd_data)

if __name__=='__main__':
    main()
