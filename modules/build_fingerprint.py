def build_tooltip_script():

    return """
    const metricColours = {
        "True Positives": "#2ECC71",
        "True Negatives": "#3498DB",
        "False Positives": "#8E44AD",
        "False Negatives": "#F39C12"
    };

    document
    .querySelectorAll(".ridge:not(.ridge-overall)")
    .forEach(ridge => {
        ridge.addEventListener(
        "mouseenter",
        () => {
            const metricColours = {
                "True Positives": "#2ECC71",
                "True Negatives": "#3498DB",
                "False Positives": "#E74C3C",
                "False Negatives": "#F39C12"
            };       

            const diffColour =
            parseFloat(ridge.dataset.diff) >= 0
                ? "#E74C3C"
                : "#2ECC71";         
        
            let insight = "";
                const diff = parseInt(
                ridge.dataset.diff
            );     

            if (
                ridge.dataset.title
                === "True Positives"
            ) {

                insight =
                    diff > 0
                    ? `ImageSNN detected ${diff} additional stego images.`
                    : `ImageCNN detected ${Math.abs(diff)} additional stego images.`;
            }

            if (
                ridge.dataset.title
                === "True Negatives"
            ) {

                insight =
                    diff > 0
                    ? `ImageSNN correctly identified ${diff} more cover images.`
                    : `ImageCNN correctly identified ${Math.abs(diff)} more cover images.`;
            }

            if (
                ridge.dataset.title
                === "False Positives"
            ) {

                insight =
                    diff > 0
                    ? `ImageSNN generated ${diff} additional false alarms.`
                    : `ImageCNN generated ${Math.abs(diff)} additional false alarms.`;
            }

            if (
                ridge.dataset.title
                === "False Negatives"
            ) {

                insight =
                    diff > 0
                    ? `ImageSNN missed ${diff} additional stego images.`
                    : `ImageSNN missed ${Math.abs(diff)} fewer stego images.`;
            }


            document.getElementById("tooltip").innerHTML = `
                <div
                    class="tooltip-title"
                    style="color:${metricColours[ridge.dataset.title]}"
                >
                    ${ridge.dataset.title}
                </div>

                <div class="tooltip-row">
                    <span class="tooltip-model">
                        ImageCNN
                    </span>

                    <span>
                        ${ridge.dataset.cnn}
                    </span>
                </div>

                <div class="tooltip-row">
                    <span class="tooltip-model">
                        ImageSNN
                    </span>

                    <span>
                        ${ridge.dataset.snn}
                    </span>
                </div>

                <hr class="tooltip-divider">

                <div class="tooltip-label">
                    Difference
                </div>

                <div
                    class="tooltip-value"
                    style="color:${diffColour}"
                >
                    ${parseInt(ridge.dataset.diff)}
                </div>

                <div class="tooltip-insight">
                    ${insight}
                </div>
            `;
        }
    );
});
"""