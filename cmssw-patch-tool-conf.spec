### RPM cms cmssw-patch-tool-conf CMSSW_5_3_23
# with cmsBuild, change the above version only when a new
# tool is added

Requires: cmssw-toolfile

# still need this (from the non-patch tool-conf spec ...
%define skipreqtools jcompiler lhapdfwrapfull lhapdffull

## IMPORT scramv1-tool-conf
