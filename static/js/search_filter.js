document.addEventListener('DOMContentLoaded', () => {
    // declare that there is something to handle
    const registerSearchButtonHandler = () => {
        const submitButton = document.getElementById('submit-button');

        submitButton.addEventListener('click', async (e) => {

            // since the submit button is not technically a part of the search bar, it has to be declared separately
            const searchInput = document.getElementById('search-bar').value;
            const response = await fetch(`/all_art/?search_filter=${(searchInput)}`);


        });
    };
    registerSearchButtonHandler();
    });