class PlaylistConverter:

    initial_append_to_xspf = ['<?xml version="1.0" encoding="UTF-8"?>', '<playlist version="1" xmlns="http://xspf.org/ns/0/">','<trackList>']
    append_to_xspf_before_title = ["<track>"]
    append_to_xspf_after_title = ["<title></title>","</track>"]
    final_append_to_xspf = ['</trackList>','</playlist>']

    def __init__(self, file_name, process, xspf_music_directory_output):
        self.file_name = file_name
        self.process = process
        self.output_lines = []
        self.xspf_music_directory_output = xspf_music_directory_output

    def get_words_from_file(self):
        f = open(self.file_name,errors='ignore')
        lines = []
        for line in f:
            line = line.rstrip()    # removes whitespace characters (\n) from the start and end of the line
            if line != "":          # if the line was only whitespace characters, skip it 
                lines.append(line)
        return lines

    def remove_directory_xspf(self, line):
        sliced_line = line[:-11]            #removes the "</location>"
        sp = sliced_line.rfind('/')         #sp is slice_position, find the first "/" from right
        sliced_line2 = sliced_line[sp:]      #remove anything before slice_position
        return sliced_line2

    def remove_directory_m3u(self, line):
        sp = line.rfind('/')         #sp is slice_position, find the first "/" from right
        sliced_line = line[sp:]     #remove anything before slice_position
        return sliced_line

    def remove_directory_wpl(self, line):
        sp = line.rfind('"')            #sp is slice_position, find the first ' " ' from right
        sliced_line = line[:sp]         #remove anything after slice_position
        if sliced_line.rfind('tid="') != -1:
            sp = sliced_line.rfind('tid="')
            sliced_line = sliced_line[:sp]         #remove anything after slice_position2
        sliced_line = sliced_line.strip('<media src="..')
        sp = sliced_line.rfind('\\')            #sp is slice_position, find the first ' " ' from right
        sliced_line = sliced_line[sp:]
        sliced_line = sliced_line.replace("\\","/")
        return sliced_line

    def add_directory_xspf(self, line):
        line = line.replace ("/", self.xspf_music_directory_output)
        line = line + "</location>"
        return line

    def add_directory_m3u(self, line):
        return line.replace ("/","/storage/emulated/0/Music/")

    def check_line_to_delete(self, line):                     #optional second way to check which line to chang/add
        substrings = ["<tracklist>", "<trackList>","<track>","<title>","<creator>","<album>","<trackNum>","<image>","</track>","</trackList>", "</playlist>", '<?xml version="1.0" encoding="UTF-8"?>', '<playlist version="1" xmlns="http://xspf.org/ns/0/">']
        return self.contains_any(line, substrings)

    def contains_any(self, line, substrings):
        return any(substring in line for substring in substrings)

    def xspf_change_directory(self):
        lines = self.get_words_from_file()
        for line in lines:
            if line.find("<location>") !=-1:
                line = self.remove_directory_xspf(line)
                line = self.add_directory_xspf(line)
            else:
                line = line.lstrip()                #strip the space left of all lines to have right indentation in following steps
            self.output_lines.append(line)
        self.output_file()

    def m3u_to_xspf(self):
        lines = self.get_words_from_file()
        lines = self.initial_append_to_xspf + lines
        self.output_lines.extend(self.initial_append_to_xspf)
        for line in lines:
            if line.find("/storage/") !=-1:
                line = self.remove_directory_m3u(line)
                self.output_lines.append(self.append_to_xspf_before_title[0])
                line = self.add_directory_xspf(line)
                self.output_lines.append(line)
                self.output_lines.extend(self.append_to_xspf_after_title)
            print(line)
        self.output_lines.extend(self.final_append_to_xspf)
        self.output_file()

    def wpl_to_xspf(self):
        lines = self.get_words_from_file()
        lines = self.initial_append_to_xspf + lines
        self.output_lines.extend(self.initial_append_to_xspf)
        for line in lines:
            if line.find("<media src=") !=-1:
                line = self.remove_directory_wpl(line)
                self.output_lines.append(self.append_to_xspf_before_title[0])
                line = self.add_directory_xspf(line)
                self.output_lines.append(line)
                self.output_lines.extend(self.append_to_xspf_after_title)
        self.output_lines.extend(self.final_append_to_xspf)
        self.output_file()

    def xspf_to_m3u(self):
        lines = self.get_words_from_file()
        for line in lines:
            if not self.check_line_to_delete(line):               #optional second way to check which line to chang/add
                if line.find("<location>") !=-1:
                    line = self.remove_directory_xspf(line)
                    line = self.add_directory_m3u(line)
                    self.output_lines.append(line)
        self.output_file()

    def output_convert_to_m3u(self):
        file_name = self.file_name.strip(".xspf")
        new_file_name = file_name + "_converted.m3u"
        with open(new_file_name, "a") as f:
            for line in self.output_lines:
                f.write(line + "\n")

    def output_convert_to_xspf(self):
        if self.file_name.endswith(".xspf"):
            file_name = self.file_name.strip(".xspf")
        if self.file_name.endswith(".m3u"):
            file_name = self.file_name.strip(".m3u")
        if self.file_name.endswith(".wpl"):
            file_name = self.file_name.strip(".wpl")
        new_file_name = file_name + "_converted.xspf"
        indentation_level = 0
        indentation_spaces = 2
        with open(new_file_name, "a") as f:
            for line in self.output_lines:
                if any(line.startswith(tags) for tags in ["<playlist","</playlist>"]):
                    indentation_level = 0
                if any(line.startswith(tags) for tags in ["<trackList>","</trackList>"]):
                    indentation_level = 1
                if any(line.startswith(tags) for tags in ["<track>","</track>"]):
                    indentation_level = 2
                if any(line.startswith(tags) for tags in ["<location>"]):
                    indentation_level = 3
                f.write(" " * indentation_level * indentation_spaces + line + "\n")


    def output_file(self):
            if self.file_name.endswith(".xspf"):
                if self.process=="Directory":
                    self.output_convert_to_xspf()
                if self.process=="Convert":
                    self.output_convert_to_m3u()
            if self.file_name.endswith(".m3u"):
                self.output_convert_to_xspf()
            if self.file_name.endswith(".wpl"):
                self.output_convert_to_xspf()

    def main(self):
        if self.file_name.endswith(".xspf"):
            if self.process=="Directory":
                self.xspf_change_directory()
            if self.process=="Convert":
                self.xspf_to_m3u()
        if self.file_name.endswith(".m3u"):
            self.m3u_to_xspf()
        if self.file_name.endswith(".wpl"):
            self.wpl_to_xspf()

    #make so that the location input doesn't require "<location>"
    #add possibility to let user to import file or list of files, all files from folder
    #add a button to add those files to a list, display the list on the right side of the GUI
    #Add a second window on the GUI to display all the playlist files selected
    #add "title" in my code to clarify strings handling ?p
    #be able to change the output location