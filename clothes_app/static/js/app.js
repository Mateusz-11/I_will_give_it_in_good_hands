document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;


            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            const choiceElement = form.querySelectorAll("#choice");
            this.selectedCategories = [];

            const institutionElement = form.querySelectorAll("#institution-choice");

            this.data = {
                bagsNumber: 0,
                addressForm: "",
                cityForm: "",
                postcodeForm: "",
                commentsForm: "",
                timeForm: "",
                phoneFormElement: "",
                dateForm: "",
                categoriesForm: "",
                organizationsForm: ""
            };

            const bagsInput = form.querySelector("input[name='bags']")
            this.bagsNumberElement = form.querySelector(".summary-bags-number")

            const addressInput = form.querySelector("input[name='address']")
            this.addressFormElement = form.querySelector(".summary-address")

            const cityInput = form.querySelector("input[name='city']")
            this.cityFormElement = form.querySelector(".summary-city")

            const postcodeInput = form.querySelector("input[name='postcode']")
            this.postcodeFormElement = form.querySelector(".summary-postcode")

            const phoneInput = form.querySelector("input[name='phone']")
            this.phoneFormElement = form.querySelector(".summary-phone")
            // console.log(phoneInput)

            const dateInput = form.querySelector("input[name='date']")
            this.dateFormElement = form.querySelector(".summary-date")
            // console.log(dateInput)

            const timeInput = form.querySelector("input[name='time']")
            this.timeFormElement = form.querySelector(".summary-time")
            // console.log(timeInput)

            const commentsInput = form.querySelector("textarea[name='comments']")
            this.commentsFormElement = form.querySelector(".summary-comments")
            // console.log(commentsInput)

            // const categoriesInput = form.querySelector("input[name='categories']")
            this.categoriesFormElement = form.querySelector(".summary-categories")
            // console.log(categoriesInput)

            // const organizationInput = form.querySelector("input[name='organization']")
            this.organizationFormElement = form.querySelector(".summary-organization")
            // console.log(organizationInput)

            // Validation Elements
            this.errormsgElementStep1 = document.querySelector("div.form-group.form-error__checkbox.hidden")
            console.log(this.errormsgElementStep1)

            this.errormsgElementStep2 = document.querySelector("div.form-group.form-error__bags.hidden")
            console.log(this.errormsgElementStep2)

            this.errormsgElementStep3 = document.querySelector("div.form-group.form-error__institution.hidden")
            console.log(this.errormsgElementStep3)

            choiceElement.forEach((element) => {
                element.addEventListener("click", (event) => {
                    if (element.checked) {
                        this.selectedCategories.push(event.target.value)
                    } else {
                        this.selectedCategories = this.selectedCategories.filter(cat => cat === event.target.value)
                    }
                })
            })

            bagsInput.addEventListener("change", (event) => {
                this.data.bagsNumber = Number(event.target.value)
            })

            addressInput.addEventListener("change", (event) => {
                this.data.addressForm = event.target.value
            })
            cityInput.addEventListener("change", (event) => {
                this.data.cityForm = event.target.value
            })
            postcodeInput.addEventListener("change", (event) => {
                this.data.postcodeForm = event.target.value
            })
            phoneInput.addEventListener("change", (event) => {
                this.data.phoneForm = event.target.value
            })

            timeInput.addEventListener("change", (event) => {
                this.data.timeForm = event.target.value
            })
            dateInput.addEventListener("change", (event) => {
                this.data.dateForm = event.target.value
            })
            commentsInput.addEventListener("change", (event) => {
                this.data.commentsForm = event.target.value
            })

            // categoriesInput.addEventListener("click", (event) => {
            //   this.data.categoriesForm = event.target.value;
            //   console.log("test click")
            // })

            choiceElement.forEach((element) => {
                element.addEventListener("click", (event) => {
                    if (element.checked) {
                        // console.log("test click")
                        this.data.categoriesForm = event.target.dataset.catname
                    }
                })
            })

            institutionElement.forEach((element) => {
                element.addEventListener("click", (event) => {
                    if (element.checked) {
                        // console.log("test click")
                        this.data.organizationsForm = event.target.dataset.orgname
                    }
                })
            })


            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }


        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    // this.currentStep++;
                    const isStepValid = this.validateForm();
                    if (isStepValid) {
                        this.currentStep++;
                    }
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        validateForm() {
            let isValid = true

            if (this.currentStep === 1) {
                const checkboxesCategory = document.querySelectorAll("input[name='categories']:checked");
                console.log(checkboxesCategory);
                if (checkboxesCategory.length === 0) {
                    // console.log(checkboxesCategory)
                    isValid = false
                    // console.log(isValid)
                }
                if (isValid) {
                }
                else {
                    this.errormsgElementStep1.classList.remove("hidden");
                    console.log(this.errormsgElementStep1)
                }
            }

            if (this.currentStep === 2) {
                const inputBags = document.querySelector("input[name='bags']").value;
                console.log(inputBags)
                if (inputBags <= 1) {
                    console.log(inputBags)
                    isValid = false
                    console.log(isValid)
                }
                if (isValid) {
                }
                else {
                    this.errormsgElementStep2.classList.remove("hidden");
                    console.log(this.errormsgElementStep2)
                }
            }

            if (this.currentStep === 3) {
                const checkboxesInstitution = document.querySelectorAll("input[name='organization']:checked");
                console.log(checkboxesInstitution);
                if (checkboxesInstitution.length === 0) {
                    // console.log(checkboxesInstitution)
                    isValid = false
                    // console.log(isValid)
                }
                if (isValid) {
                }
                else {
                    this.errormsgElementStep3.classList.remove("hidden");
                    console.log(this.errormsgElementStep3)
                }
            }

            return isValid;
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;
            this.selectedInstitution = [];


            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (Number(slide.dataset.step) === this.currentStep) {
                    slide.classList.add("active");
                }
            });


            if (this.currentStep === 3) {
                const institutionEl = document.querySelectorAll("#institution");
                institutionEl.forEach((elDiv) => {
                    const institutionCategories = elDiv.dataset.id.split(" ")
                    if (this.selectedCategories.some(selectedCategory => institutionCategories.includes(selectedCategory))) {
                        elDiv.style.display = "block"
                    } else {
                        elDiv.style.display = "none"
                    }
                })
            }

            if (this.currentStep === 4) {
                // console.log('step4')
            }
            if (this.currentStep === 5) {
                this.bagsNumberElement.textContent = this.data.bagsNumber.toString()
                // console.log(this.bagsNumberElement)
                this.addressFormElement.textContent = this.data.addressForm.toString()
                this.cityFormElement.textContent = this.data.cityForm.toString()
                this.postcodeFormElement.textContent = this.data.postcodeForm.toString()
                this.phoneFormElement.textContent = this.data.phoneForm.toString()

                this.dateFormElement.textContent = this.data.dateForm.toString()
                this.timeFormElement.textContent = this.data.timeForm.toString()
                this.commentsFormElement.textContent = this.data.commentsForm.toString()
                this.categoriesFormElement.textContent = this.data.categoriesForm.toString()
                // console.log(this.categoriesFormElement)
                this.organizationFormElement.textContent = this.data.organizationsForm.toString()
                // console.log(this.organizationFormElement)

            }

            if (this.currentStep === 6) {
                // console.log('step6')
            }

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            // e.preventDefault();
            this.currentStep++;
            this.updateForm();
            // console.log("Wysylam", this.currentStep)
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
});
