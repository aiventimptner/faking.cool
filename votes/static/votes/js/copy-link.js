document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.copy-link').forEach(($button) => {
        let $input = $button.parentElement.parentElement.querySelector('input');

        $button.addEventListener('click', async () => {
            $input.select();
            document.execCommand('copy');

            let value = $input.value;

            $input.setAttribute("disabled", "");
            $button.setAttribute("style", "border: 0;");
            $button.classList.add("is-static");
            $input.value = "Kopiert!";

            await new Promise(resolve => setTimeout(resolve, 1500));

            $input.value = value;
            $button.classList.remove("is-static");
            $button.removeAttribute("style");
            $input.removeAttribute("disabled");
        });
    }));
});