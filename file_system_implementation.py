class FileSystem:
    def __init__(self):
        self.root = Directory("/")

    def create_directory(self, path):
        nodes = path[1:].split("/")
        end_path=nodes[-1]
        other_nodes = nodes[:-1]
        last_node_before = self._find_bottom_node(other_nodes)

        if not isinstance(last_node_before, Directory):
            raise ValueError(f"{end_path} is not a directory")
        else :
            new_directory = Directory(end_path)
            last_node_before.add_node(new_directory)
        print('Created a new directory')
        

    def create_file(self, path, contents):
        nodes = path[1:].split("/")
        end_path=nodes[-1]
        other_nodes = nodes[:-1]
        last_node_before = self._find_bottom_node(other_nodes)

        if not isinstance(last_node_before, Directory):
            raise ValueError(f"{end_path} is not a directory")
        else :
            new_file = File(end_path)
            last_node_before.add_node(new_file)
            new_file.write_contents(contents)
        print('Created a new File')

    def read_file(self, path):
        nodes = path[1:].split("/")
        end_path=nodes[-1]
        last_node = self._find_bottom_node(nodes)

        if not isinstance(last_node, File):
            raise ValueError(f"{last_node.name} is not a File")
        else :
            return last_node.contents

    def delete_directory_or_file(self, path):
        nodes = path[1:].split("/")
        end_path=nodes[-1]
        other_nodes = nodes[:-1]
        last_node_before = self._find_bottom_node(other_nodes)
        
        children_names = []
        for child in last_node_before.children:
            children_names.append(child.name)
        if not end_path in children_names:
            raise ValueError("c'est nul !")
        
        last_node_before.delete_node(end_path)
        print('Node successfully deleted.')


    def size(self):
        size=0
        nodes = [self.root]
        while len(nodes) >0:
            current_node= nodes.pop()
            if isinstance(current_node,Directory):
                nodes.extends(current_node.children)
                continue
            if isinstance(current_node, File):
              size+=len(current_node)
        return size


    def __str__(self):
        return f"*** FileSystem ***\n" + self.root.__str__() + "\n***"
    
    @staticmethod
    def _validate_path(path):
        if not path.startswith("/"):
            raise ValueError("Path should start with `/`.")


    def _find_bottom_node(self, node_names):
        current_node = self.root
        for node_name in node_names:
          if node_name in current_node.children:
            current_node = current_node.children[node_name]
          else : 
            raise Exception('not so goood bro')
        return current_node

      


class Node:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name} ({type(self).__name__})"


class Directory(Node):
    def __init__(self, name):
        super().__init__(name)
        self.children = {}

    def add_node(self, node):
        self.children[node.name] = node

    def delete_node(self, name):
        del self.children[name]

    def __str__(self):
        string = super().__str__()

        children_strings = []
        for child in list(self.children.values()):
            child_string = child.__str__().rstrip()
            children_strings.append(child_string)

        children_combined_string = indent("\n".join(children_strings), 2)
        string += "\n" + children_combined_string.rstrip()
        return string


class File(Node):
    def __init__(self, name):
        super().__init__(name)
        self.contents = ""

    def write_contents(self, contents):
        self.contents = contents

    def __len__(self):
        return len(self.contents)

    def __str__(self):
        return super().__str__() + f" | {len(self)} characters"


def indent(string, number_of_spaces):
    spaces = " " * number_of_spaces
    lines = string.split("\n")
    indented_lines = [spaces + line for line in lines]
    return "\n".join(indented_lines)
