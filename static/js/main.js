console.log("BugMind AI is running successfully!");


document.addEventListener(
    "DOMContentLoaded",
    function () {


        const menuButton = document.querySelector(
            ".mobile-menu-button"
        );


        const sidebar = document.querySelector(
            ".sidebar"
        );


        const closeButton = document.querySelector(
            ".sidebar-close"
        );


        const overlay = document.querySelector(
            ".sidebar-overlay"
        );


        // Open mobile sidebar

        if (
            menuButton &&
            sidebar &&
            overlay
        ) {

            menuButton.addEventListener(
                "click",
                function () {

                    sidebar.classList.add(
                        "sidebar-open"
                    );

                    overlay.classList.add(
                        "active"
                    );

                }
            );

        }


        // Close button

        if (
            closeButton &&
            sidebar &&
            overlay
        ) {

            closeButton.addEventListener(
                "click",
                function () {

                    sidebar.classList.remove(
                        "sidebar-open"
                    );

                    overlay.classList.remove(
                        "active"
                    );

                }
            );

        }


        // Close when clicking outside

        if (
            overlay &&
            sidebar
        ) {

            overlay.addEventListener(
                "click",
                function () {

                    sidebar.classList.remove(
                        "sidebar-open"
                    );

                    overlay.classList.remove(
                        "active"
                    );

                }
            );

        }


        // Close sidebar when a navigation link is clicked

        const navLinks = document.querySelectorAll(
            ".sidebar-nav .nav-item"
        );


        navLinks.forEach(
            function (link) {

                link.addEventListener(
                    "click",
                    function () {

                        if (
                            window.innerWidth <= 768
                        ) {

                            sidebar.classList.remove(
                                "sidebar-open"
                            );

                            overlay.classList.remove(
                                "active"
                            );

                        }

                    }
                );

            }
        );


        // Close sidebar if screen changes to desktop size

        window.addEventListener(
            "resize",
            function () {

                if (
                    window.innerWidth > 768 &&
                    sidebar &&
                    overlay
                ) {

                    sidebar.classList.remove(
                        "sidebar-open"
                    );

                    overlay.classList.remove(
                        "active"
                    );

                }

            }
        );


    }
);