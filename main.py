import os
import logging


def _setup_logger():
    """
    Sets up a logger for the class.

    Returns:
        logging.Logger: A configured logger.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


class XcodeProjectAnalyzer:
    """
    A class to analyze Xcode projects by extracting relevant code for AI analysis.

    Attributes:
        base_folder (str): The base directory where Xcode projects are located.
        relevant_extensions (list): List of file extensions considered relevant for analysis.
        logger (logging.Logger): Logger for the class.
    """

    def __init__(self, project_folder):
        """
        The constructor for XcodeProjectAnalyzer class.

        Parameters:
            project_folder (str): The base directory where Xcode projects are located.
        """
        self.base_folder = project_folder
        self.relevant_extensions = ['.swift', '.h', '.m']
        self.logger = _setup_logger()

    def select_project(self):
        """
        Lists and allows the user to select the Xcode project from the base directory.

        Returns:
            str: The selected project name.
        """
        repositories = [d for d in os.listdir(self.base_folder) if os.path.isdir(os.path.join(self.base_folder, d))]
        self.logger.info("Available Projects:")
        for i, repository in enumerate(repositories):
            self.logger.info(f"{i+1}. {repository}")

        choice = int(input("Select a project (number): ")) - 1
        return repositories[choice]

    def analyze_project(self, project_name):
        """
        Analyzes the selected project by extracting relevant file contents.

        Parameters:
            project_name (str): The name of the project to analyze.
        """
        project_path = os.path.join(self.base_folder, project_name)
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if any(file.endswith(ext) for ext in self.relevant_extensions):
                    print(file.title())
                    self.process_file(os.path.join(root, file), project_name)

    def process_file(self, file_path, project_name):
        """
        Processes each relevant file in the project.
        ...
        """
        try:
            with open(file_path, 'r') as file:
                content = file.readlines()
                filtered_content = self.filter_comments(content)
                category = self.categorize_file(file_path, project_name)
                self.output_content(file_path, filtered_content, project_name, category)
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {e}")

    @staticmethod
    def filter_comments(lines):
        """
        Filters comments and documentation strings from the file content.

        Parameters:
            lines (list): List of lines in the file.

        Returns:
            list: Filtered list of lines without comments and docstrings.
        """
        return [line for line in lines if not line.strip().startswith(("//", "/*", "*", "*/", "///"))]

    def categorize_file(self, file_path, project_name):
        """
        Categorizes the file based on its internal folder structure.

        Parameters:
            file_path (str): The path to the file.
            project_name (str): The name of the project.

        Returns:
            str: The category of the file.
        """
        relative_path = os.path.relpath(file_path, start=os.path.join(self.base_folder, project_name))
        category = os.path.dirname(relative_path)
        return category if category else "Root"

    def output_content(self, file_path, content, project_name, category):
        """
        Outputs the content of a file to a text file in the project directory.

        Parameters:
            file_path (str): The path to the file.
            content (list): The content of the file.
            project_name (str): The name of the project.
            category (str): The category of the file.
        """
        output_file = os.path.join(self.base_folder, project_name, f"{project_name}_code_review.txt")
        try:
            with open(output_file, 'a') as file:
                file.write(f"Category: {category}\nFile: {file_path}\n")
                file.write(f"Content:\n{''.join(content)}\n\n")
        except Exception as e:
            self.logger.error(f"Error writing to output file {output_file}: {e}")


if __name__ == "__main__":
    base_folder = "/Users/fowenati/dev/xcode"  # Replace with your folder path
    analyzer = XcodeProjectAnalyzer(base_folder)
    project = analyzer.select_project()
    analyzer.analyze_project(project)
