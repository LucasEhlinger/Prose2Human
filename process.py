import os, shutil, re, json, glob
from datetime import datetime

absolute_path = os.path.dirname(__file__)


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


def clean_processing():
    # Empty processing failure
    folder = os.path.join(absolute_path, 'Processing/')
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


clean_processing()

# Copy calendars to Processing
toProcess = listdir_nohidden(os.path.join(absolute_path, 'toProcess/'))
if len(toProcess) == 0:
    print("Nothing to process")
    exit(0)
elif len(toProcess) > 1:
    print("Can process file only 1 by 1")
    exit(0)

print("Start processing")

# take last .ics in toProcess
files = [f for f in toProcess]
if not re.match(r".+\.ics", files[0]):
    print(".ics file needed")
    exit(0)

# copy in history with datetime_before sufix
shutil.copyfile(files[0],
                os.path.join(absolute_path, "History/Import_" + datetime.now().strftime("%Y_%m_%d@%H:%M:%S") + ".ics"))

# move .ics to Processing
shutil.move(files[0], os.path.join(absolute_path, "Processing/Calendar.ics"))

# loading configuration
# Opening JSON file
with open(os.path.join(absolute_path, 'config.json')) as json_file:
    config = json.load(json_file)

# rename elements in .ics folowing config.json file
regex = r"SUMMARY;LANGUAGE=fr:(.+)"
with open(os.path.join(absolute_path, 'Processing/Result.ics'), 'a') as output:
    with open(os.path.join(absolute_path, 'Processing/Calendar.ics')) as WIP:
        while True:
            line = WIP.readline()
            if not line:
                break
            match = re.match(regex, line)
            if match and match.groups()[0] in config:
                line = re.sub(regex, "SUMMARY;LANGUAGE=fr:" + config[match.groups()[0]], line)

            output.writelines(line)
    WIP.close()
output.close()
print("EOF")

# copy in history with datetime_after suffix
shutil.copyfile(os.path.join(absolute_path, 'Processing/Result.ics'),
                os.path.join(absolute_path,
                             "History/Processed_" + datetime.now().strftime("%Y_%m_%d@%H:%M:%S") + ".ics"))

# move in Web with rename of calendar.ics

shutil.copyfile(os.path.join(absolute_path, 'Processing/Result.ics'), os.path.join(absolute_path, "Web/Calendar.ics"))

# delete files in ToProcess
clean_processing()
