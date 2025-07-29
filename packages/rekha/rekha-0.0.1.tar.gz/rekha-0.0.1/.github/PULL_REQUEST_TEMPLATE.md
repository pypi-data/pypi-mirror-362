FILL IN THE PR DESCRIPTION HERE

FIX #xxxx (*link existing issues this PR will resolve*)

**BEFORE SUBMITTING, PLEASE READ THE CHECKLIST BELOW AND FILL IN THE DESCRIPTION ABOVE**

---

<details>
<!-- inside this <details> section, markdown rendering does not work, so we use raw html here. -->
<summary><b> PR Checklist (Click to Expand) </b></summary>

<p>Thank you for your contribution to Rekha! Before submitting the pull request, please ensure the PR meets the following criteria. This helps Rekha maintain the code quality and improve the efficiency of the review process.</p>

<h3>PR Title and Classification</h3>
<p>Only specific types of PRs will be reviewed. The PR title is prefixed appropriately to indicate the type of change. Please use one of the following:</p>
<ul>
    <li><code>[Bugfix]</code> for bug fixes.</li>
    <li><code>[CI/Build]</code> for build or continuous integration improvements.</li>
    <li><code>[Doc]</code> for documentation fixes and improvements.</li>
    <li><code>[Plot]</code> for adding a new plot type or improving an existing plot type. Plot name should appear in the title.</li>
    <li><code>[API]</code> for changes to the public API.</li>
    <li><code>[Core]</code> for changes in the core plotting logic.</li>
    <li><code>[Theme]</code> for changes to styling, theming, or visual appearance.</li>
    <li><code>[Performance]</code> for performance improvements.</li>
    <li><code>[Misc]</code> for PRs that do not fit the above categories. Please use this sparingly.</li>
</ul>
<p><strong>Note:</strong> If the PR spans more than one category, please include all relevant prefixes.</p>

<h3>Code Quality</h3>

<p>The PR needs to meet the following code quality standards:</p>

<ul>
    <li>Pass all linter checks. Please use <code>make format</code> and <code>make lint</code> to format and check your code.</li>
    <li>Pass all existing tests. Run <code>make test</code> to verify.</li>
    <li>Include tests for new functionality. All new features should have corresponding tests.</li>
    <li>The code needs to be well-documented with clear docstrings and comments.</li>
    <li>Please add documentation to <code>docs/</code> if the PR modifies user-facing behaviors of Rekha. This helps users understand and utilize new features or changes.</li>
</ul>

<h3>Plot-Specific Requirements</h3>
<p>If your PR adds or modifies plot functionality:</p>
<ul>
    <li>Include example usage in the <code>examples/</code> directory.</li>
    <li>Ensure the plot works with both light and dark themes.</li>
    <li>Test with various data types and edge cases.</li>
    <li>Verify export functionality works correctly.</li>
    <li>Update relevant documentation and user guides.</li>
</ul>

<h3>Notes for Large Changes</h3>
<p>Please keep the changes as concise as possible. For major architectural changes (>500 LOC), we would expect a GitHub issue (RFC) discussing the technical design and justification. Otherwise, we will tag it with <code>rfc-required</code> and might not go through the PR.</p>

<h3>Testing</h3>
<p>Please ensure your changes are properly tested:</p>
<ul>
    <li><code>make test</code> - Run all unit and integration tests</li>
    <li>Manual testing with various data types and sizes</li>
    <li>Test both programmatic usage and interactive use cases</li>
</ul>

<h3>Documentation</h3>
<p>If your PR affects user-facing functionality:</p>
<ul>
    <li>Update relevant docstrings with proper type hints</li>
    <li>Add or update examples in the documentation</li>
    <li>Update the user guide if introducing new concepts</li>
    <li>Run <code>make docs</code> to ensure documentation builds correctly</li>
</ul>

<h3>Thank You</h3>

<p>Finally, thank you for taking the time to read these guidelines and for your interest in contributing to Rekha. Your contributions make Rekha a great tool for everyone!</p>

</details>