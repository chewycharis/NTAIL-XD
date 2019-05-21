#!/bin/bash 
cd ~/Desktop
protein='NIV-NTAIL-XD'
directory='/home/chuhui/Desktop'
chimera 0-renumber.py $directory $protein'.pdb'
pymol 1-cap.py $directory $protein'_renumber.pdb'
python 2-compare_atoms.py $directory $protein'_renumber_cap.pdb' 'merged.rtp'
mv $protein'.pdb' $protein'_preprocessed.pdb'
rm $protein'_renumber.pdb'
rm $protein'_renumber_cap.pdb'
mv $protein'_renumber_cap_corrected.pdb' $protein'.pdb'


