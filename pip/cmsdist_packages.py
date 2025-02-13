def packages(virtual_packages, *args):
  from re import match
  from os.path import dirname,join, exists
  import os, sys, platform
  pkg_dir = dirname(__file__)
  req = join(pkg_dir,'requirements.txt')
  if not exists(req): return
  extra_match = {}
  extra_match['platform_machine'] = platform.machine()
  extra_match['sys_platform'] = sys.platform
  extra_match['os_name'] = os.name
  for line in [ l.strip().replace(' ','') for l in open(req).readlines()]:
    if line.startswith('#'):continue
    if not '==' in line: continue
    items = line.strip().split(';')
    (pkg, ver) = items[0].strip().split('==',1)
    matched=True
    for item in items[1:]:
      m = match("^("+"|".join(list(extra_match.keys()))+")(==|!=)'([^']+)'$", item)
      if m:
        if m.group(2)=='==' and extra_match[m.group(1)]!=m.group(3): matched=False
        if m.group(2)=='!=' and extra_match[m.group(1)]==m.group(3): matched=False
    if matched:
      virtual_packages['py3-'+pkg]='%s/package.sh "py3-%s" "%s" "py3"' % (pkg_dir, pkg, ver)
  return
