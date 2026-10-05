## Introduction

This repository, Flask and Furious, was modified off the Open Coding Society `Pages` repository and was developed by Ruchika Kench, Akshara Shankar, and Avantika Chittari.

This project was created for Safe Passage Heals, a nonprofit which hosts workshops and events to assist women and children who have experienced domestic violence.

Our project contains a dynamic event calendar, login system, admin event management dashboard, and an interactive path to recovery simulation integrated with quizzes, surveys, and an AI chatbot (registered Gemini API key).

All frontend content for our Dynamic Media Management and Interactive Path to Recovery Simulation project components can be found in the folder "safepassageheals"

---

## License
We have an Apache 2.0 License for our frontend, the same as the root Open Coding Society repository.

## Locations
All content for the website pages of our project are located in the safepassageheals folder, with fixed site templates and layouts are located in _sass/minima

--- 

### Development Environment Setup

Comprehensive start. A topic-by-topic guide to getting this project running is published [here](https://pages.opencodingsociety.com/tools/).

Quick start.  A quick start below is a reminder, but is dependent on your knowledge.  Only follow this instruction if you need a refresher.  Always default to the comprehensive start if any problem occurs.

#### Clone Repo

Run these commands to obtain the project, then locate into the project directory with the terminal, install an extensive set of tools, and make.

```bash
git clone <this-repo> # git clone https://github.com/open-coding-society/pages.git 
cd <repo-dir>/scripts # cd pages 
```

#### Windows WSL and/or Ubuntu or Kali Users

- Execute the script: `./activate_ubuntu.sh` or `./activate_kali.sh`

#### macOS Users

- Execute the script: `./activate_macos.sh`

#### Kasm Cloud Desktop Users

- Execute the script: `./activate_github.sh`

## Run Server on localhost

To preview the project you will need to "make" the project.

### Bundle install

The very first time you clone run project you will need to run this Ruby command as the final part of your setup.

```bash
bundle install
```

### Jupyter Kernels

To run many of the IPYNB files you will need to install Jupyter kernels for the languages you want to use. Here are the most common and recommended kernels:

#### Recommended Kernels

- **Python3** (ipykernel): For Python code cells and most data science workflows.
- **Java** (IJava or jbang-ijava): For Java code cells and Java notebooks.
- **JavaScript** (tslab): For JavaScript code cells and JavaScript notebooks.

#### Installing tslab

First, Install tslab
```
npm install -g tslab
```

Second, confirm it's installed
```
tslab install --version
```

Finally, register it to your Jupyter environment
```
tslab install
```

#### Installing IJava or JBang

**macOS (Homebrew):**

```bash
# For Java kernel (IJava)
brew install coursier
cs install --channel=https://github.com/SpencerPark/IJava/releases/latest/download/channel.json ijava
# Or for jbang-ijava
brew install jbang
jbang app install ijava
```

**Ubuntu/Linux (apt):**

```bash
# For Java kernel (IJava)
sudo apt install coursier
cs install --channel=https://github.com/SpencerPark/IJava/releases/latest/download/channel.json ijava

# Or for jbang-ijava
sudo apt install jbang
# or sudo snap install jbang --classic
jbang app install ijava
```

#### List your installed kernels

```shell
(venv) username@machine path % jupyter kernelspec list
Available kernels:
  python3        /Users/username/Library/Jupyter/kernels/python3
  java           /Users/username/Library/Jupyter/kernels/java
  jbang-ijava    /Users/username/Library/Jupyter/kernels/jbang-ijava
  jslab          /Users/username/Library/Jupyter/kernels/jslab
  tslab          /Users/username/Library/Jupyter/kernels/tslab
```

Recommended Kernels

### Start the Server  

This requires running terminal commands `make`, `make stop`, `make clean`, or `make convert` to manage the running server.  Logging of details will appear in the terminal.   A `Makefile` has been created in the project to support commands and start processes.

Start the server, this is the best choice for initial and iterative development.  Note. after the initial `make`, you should see files automatically refresh in the terminal on VSCode save.

  ```bash
  make
  ```

For easier build failure logging, run:

```bash
python _projects/make-helper/run_make.py
```

### Load web application into the Browser

Start the preview server in the terminal,
The terminal output from `make` shows the server address. "Cmd" or "Ctl" click the http location to open the preview server in a browser. Here is an example Server address message, click on the Server address to load:...

  ```text
  http://0.0.0.0:4500/pages/
  ```

### Regeneration of web application

Save on ".ipynb" or ".md" file activiates "regeneration". An example terminal message is below.  Refresh the browser to see updates after the message displays.

  ```text
  Regenerating: 1 file(s) changed at 2023-07-31 06:54:32
      _notebooks/2024-01-04-cockpit-setup.ipynb
  ```

### Other "make" commands

Terminal messages are generated from background processes.  At any time, click return or enter in a terminal window to obtain a prompt.  Once you have the prompt you can use the terminal as needed for other tasks.  Always return to the root of project `cd ~/open/pages` for all "make" actions.

#### Stop the preview server

Stopping the server ends the web server applications running process.  However, it leaves constructed files in the project in a ready state for the next time you run `make`.

  ```bash
  make stop
  ```

### Clean the local web application environment

This command will top the server and "clean" all previously constructed files (ie .ipynb -> .md). This is the best choice when renaming files has created duplicates that are visible when previewing work.

  ```bash
  make clean
  ```

### Observe build errors

Test Jupyter Notebook conversions (ie .ipynb -> .md), this is the best choice to see if an IPYNB conversion error is occurring.

  ```bash
  make convert
  ```

---

## Development Support

### Navigation Bar

To add pages to the top navigation bar use _config.yml to order and determine which menus you want and how to order them.  Review the_config.yml in this project for an example.

Our custom navigation bar css is located under /assets/screenQueue/style/navbar.css

### Blog Page

There is a blog page that has options for images and a description of the page. This page can help the viewer understand what the page is about and what they can expect to find on the page. The way to add images to a page is to have the following front matter `image: /images/file.jpg` and then the name of the image that you want to use. The image must be in the `images` folder. Furthermore, if you would like the file to not show up on the blog page `hide: true` can be added to the front matter.


### Layouts

- To use or create a custom page layout, make an HTML page inside the _layouts directory, and when you want to use that layout in a file, use the following front matter `layout: [your layout here]`.  All layouts will be written in liquid to define the structure of the page.

### Metadata

Metadata, also known as "front matter", is a set of key-value pairs that can provide additional information to GitHub Pages about .md and .ipynb files. This can and probably will be used in other file types (ie doc, pdf) if we add them to the system.

In the front matter, you can also define things like a title and description for the page.  Additional front matter is defined to place content on the "Computer Science Lab Notebook" page.  The `courses:` key will place data on a specific page with the nested `week:` placing data on a specific row on the page.  The `type:` key in "front matter" will place the blog under the plans, hacks(ToDo), and tangibles columns.

- In our files, the front matter is defined at the top of the page or the first markdown cell.

  - First, open one of the .md or .ipynb files already included in either your _posts|_notebooks folder.

  - In the .md file, you should notice something similar to this at the top of the page. To see this in your .ipynb files you will need to double-click the markdown cell at the top of the file.

  - Here is our default frontmatter for our pages

  ```yaml
  ---
  layout: post
  title: Feature Name
  permalink: /sph/featurename/
  show_reading_time: false
  ---
  ```
---

## Future Plans
1. AI-Powered Emotional Support Enhancement
Enhance the confidential AI assistant with more advanced natural language processing so it can provide more empathetic, personalized, and resource-focused responses while maintaining privacy and safety standards.
2. Data-Driven Wellness Scale System
Replace multiple-choice quizzes with 1–5 scale assessments to better measure user emotions, confidence, and recovery progress. Aggregated data can help identify common challenges and improve support resources.
3. Machine Learning Risk & Resource Recommendation
Use machine learning to analyze quiz and interaction patterns to recommend personalized resources, support strategies, or next steps based on user needs and recovery stage.
4. Recovery Progress Tracking Dashboard
Develop an optional private dashboard where users can monitor their progress over time through quiz trends, completed modules, and personal wellness indicators.
5. Predictive Event Planning Analytics
Collect anonymous event attendance and engagement data to help Safe Passage Heals predict which workshops or support events are most needed, improving scheduling and outreach.
6. Multilingual AI and Accessibility Expansion
Expand the platform with multilingual support and accessibility tools such as voice assistance, translation, and screen-reader optimization to reach more diverse communities.
7. Expanded Interactive Simulation Paths
Add more scenarios and branching storylines to Path to Recovery, allowing users to experience different domestic violence situations and support pathways for more realistic and personalized learning.
8. Community Impact & Research Insights
Use anonymized platform data from quizzes and interactions to generate reports and visual insights for Safe Passage Heals, helping the organization better understand community needs and evaluate program impact over time.


