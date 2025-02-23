<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MasterEye - IP Scanner</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
            background-color: #f4f4f4;
        }
        h1, h2, h3 {
            color: #333;
        }
        code {
            background: #ddd;
            padding: 3px 6px;
            border-radius: 5px;
        }
        pre {
            background: #ddd;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        .container {
            max-width: 800px;
            margin: auto;
            background: white;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        img {
            max-width: 100%;
            height: auto;
            margin: 10px 0;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>MasterEye - IP Scanner</h1>

    <img src="./screenshot.png" alt="MasterEye Screenshot">

    <p><em>A powerful multi-threaded IP scanner with port scanning, credential testing, and a user-friendly GUI.</em></p>

    <h2>Features</h2>
    <ul>
        <li>Scan an IP range for active hosts</li>
        <li>Check for open ports (default: 80, 443, 8080)</li>
        <li>Attempt login with default credentials</li>
        <li>Multi-threaded scanning for speed</li>
        <li>Export results in CSV & JSON formats</li>
        <li>Dark theme support</li>
    </ul>

    <h2>Installation</h2>
    <h3>Prerequisites</h3>
    <p>Ensure you have Python 3 installed. You can check by running:</p>
    <pre><code>python --version</code></pre>

    <h3>Clone the Repository</h3>
    <pre><code>git clone https://github.com/yourusername/MasterEye.git
cd MasterEye</code></pre>

    <h3>Install Dependencies</h3>
    <pre><code>pip install -r requirements.txt</code></pre>

    <h2>Running the Application</h2>
    <pre><code>python mastereye.py</code></pre>

    <h2>Dependencies</h2>
    <p>The application requires the following Python libraries:</p>
    <ul>
        <li><code>tkinter</code> (GUI)</li>
        <li><code>socket</code> (Network communication)</li>
        <li><code>ipaddress</code> (IP range handling)</li>
        <li><code>threading</code> (Multi-threading support)</li>
        <li><code>requests</code> (HTTP requests for login attempts)</li>
        <li><code>csv</code> & <code>json</code> (Exporting results)</li>
        <li><code>queue</code> (Thread-safe data handling)</li>
    </ul>

    <h2>Usage</h2>
    <ol>
        <li>Enter an IP range (e.g., <code>192.168.1.1-192.168.1.255</code>).</li>
        <li>Click <strong>Start Scan</strong> to begin scanning.</li>
        <li>View live scan results in the table.</li>
        <li>Export results to CSV or JSON.</li>
        <li>Toggle dark mode in the settings menu.</li>
    </ol>

    <h2>Screenshots</h2>
    <img src="./screenshot.png" alt="MasterEye GUI">

    <h2>Contributing</h2>
    <p>Feel free to fork this repository and submit pull requests for improvements!</p>

    <h2>License</h2>
    <p>This project is licensed under the MIT License.</p>
</div>

</body>
</html>
