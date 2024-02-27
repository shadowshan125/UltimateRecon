import os
import logging
import subprocess
import time

DEFAULT_OUTPUT_DIR = "reconoutput"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to run a specific reconnaissance tool
def run_tool(tool, base_url, output_file):
    try:
        subprocess.run([tool, base_url, "-o", output_file], check=True)
        logger.info(f"Successfully ran {tool} and saved output to {output_file}")
    except FileNotFoundError:
        logger.error(f"Error running {tool}: {tool} is not installed or not available in PATH")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running {tool}: {e}")
    except Exception as e:
        logger.error(f"An error occurred while running {tool}: {e}")

# Function to run Katana tool
def run_katana(base_url, output_file):
    tool = "katana"
    try:
        subprocess.run([tool, "-u", base_url, "-o", output_file], check=True)
        logger.info(f"Successfully ran {tool} and saved output to {output_file}")
        return output_file
    except FileNotFoundError:
        logger.error(f"Error running {tool}: {tool} is not installed or not available in PATH")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running {tool}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while running {tool}: {e}")

# Function to run Amass tool
def run_amass(base_url, output_file):
    tool = "amass"
    try:
        subprocess.run([tool, "enum", "-d", base_url, "-o", output_file], check=True)
        logger.info(f"Successfully ran {tool} and saved output to {output_file}")
        return output_file
    except FileNotFoundError:
        logger.error(f"Error running {tool}: {tool} is not installed or not available in PATH")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running {tool}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while running {tool}: {e}")

# Function to run Sublist3r tool
def run_sublist3r(base_url, output_file):
    tool = "sublist3r"
    try:
        subprocess.run([tool, "-d", base_url, "-o", output_file], check=True)
        logger.info(f"Successfully ran {tool} and saved output to {output_file}")
        return output_file
    except FileNotFoundError:
        logger.error(f"Error running {tool}: {tool} is not installed or not available in PATH")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running {tool}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while running {tool}: {e}")

# Function to concatenate multiple files into one
def concatenate_files(input_files, output_file):
    with open(output_file, 'w') as outfile:
        for input_file in input_files:
            with open(input_file, 'r') as infile:
                outfile.write(infile.read())

# Main function to run the reconnaissance tool
def run_reconnaissance(base_url, output_dir=None):
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR

    os.makedirs(output_dir, exist_ok=True)
    
    start_time = time.time()

    # Update the output file paths for each tool
    katana_output_file = run_katana(base_url, os.path.join(output_dir, f"{base_url}_katana_output.txt"))
    amass_output_file = run_amass(base_url, os.path.join(output_dir, f"{base_url}_amass_output.txt"))
    sublist3r_output_file = run_sublist3r(base_url, os.path.join(output_dir, f"{base_url}_sublist3r_output.txt"))



    # Run each reconnaissance tool
    run_katana(base_url, katana_output_file)
    run_amass(base_url, amass_output_file)
    run_sublist3r(base_url, sublist3r_output_file)

    # Consolidate outputs into a single file
    consolidated_output_file = os.path.join(output_dir, f"{base_url}_reconOutput.txt")
    concatenate_files([katana_output_file, amass_output_file, sublist3r_output_file], consolidated_output_file)

    logger.info(f"All reconnaissance completed. Consolidated output saved to {consolidated_output_file}")
            
    end_time = time.time()
    total_time = end_time - start_time
    logger.info(f"All reconnaissance completed in {total_time:.2f} seconds. Consolidated output saved to {consolidated_output_file}")



if __name__ == "__main__":
    base_url_option = input("Enter the base URL or leave blank to skip: ").strip()
    run_reconnaissance(base_url_option)


