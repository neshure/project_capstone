console.log('main.js loaded');
const Confirm = {
  open(options) {
    options = Object.assign({}, {
    }, options);

    const html = `
    <div class="confirm">
      <div class="confirm__window">
        <div class="confirm__titlebar">
          <span class="confirm__title">${options.title}</span>
        </div>
        <div class="confirm__content">${options.message}<div class="confirm__button">
            <button class="confirm__button confirm__button--ok confirm__button--fill">${options.okText}</button>
            <button class="confirm__button confirm__button--cancel">${options.cancelText}</button>
          </div>
        </div>
      </div>
    </div>
    `;
    const template = document.createElement('template');
    template.innerHTML = html;
    
    
    const confirmElement = template.content.querySelector('.confirm');
    const okButton = template.content.querySelector('.confirm__button--ok');
    const cancelButton = template.content.querySelector('.confirm__button--cancel');


    okButton.addEventListener('click', () => {
      options.onOk();
      this._close(confirmElement);
    });

    cancelButton.addEventListener('click', () => {
      options.onCancel();
      this._close(confirmElement);
    });

      
    document.body.appendChild(template.content);

  },

};