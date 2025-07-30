import streamlit.components.v1 as components


def allow_blank_navigation():
    """Allow links embedded in iframes to open in the same tab (target='_parent' or '_blank')"""

    components.html('''<script language="javascript">
                    var reloadRequired = false;
                    var iframesToReload = []
                    document.addEventListener('DOMContentLoaded', () => {
                    // Function to update the sandbox attribute
                    function updateSandboxAttribute(iframe) {
                        console.log('updating an iframe!');
                        let sandboxAttr = iframe.getAttribute('sandbox') || '';
                        if (!sandboxAttr.includes('allow-top-navigation')) {
                            iframe.setAttribute('sandbox', sandboxAttr + ' allow-top-navigation');
                            reloadRequired = true;
                            iframesToReload.push(iframe);
                            console.log(`Updated sandbox attribute for iframe with src: ${iframe.src}`);
                            
                        }
                    }

                    // Function to check and update all iframes in a node
                    function checkAndUpdateIframes(node) {
                    console.log('node', node.tagName);
                        if (node.tagName === 'IFRAME') {
                            updateSandboxAttribute(node);
                        } else if (node.querySelectorAll) {
                            node.querySelectorAll('iframe').forEach(updateSandboxAttribute);
                        }
                    }

                    // Create a MutationObserver to detect added iframes
                    const observer = new MutationObserver((mutations) => {
                        mutations.forEach(mutation => {
                            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                                mutation.addedNodes.forEach(node => {
                                    checkAndUpdateIframes(node);
                                });
                            }
                        });
                    });

                    // Start observing the document body for added iframes
                    observer.observe(parent.document.body, {
                        childList: true,
                        subtree: true
                    });

                    // Initially update existing iframes
                    parent.document.querySelectorAll('iframe').forEach(updateSandboxAttribute);

                    console.log('Mutation observer set up and initial iframes updated.');

                    if (reloadRequired) {
                        console.log('reloading')
                        setTimeout(function() {
                            for (var i = 0; i < iframesToReload.length; i++) {
                                iframesToReload[i].contentWindow.location.reload();
                            }
                        }, 300)
                    }
                });
                    </script>
                    ''', height=0)

    # components.html('''<script language="javascript">
    #                 document.addEventListener('DOMContentLoaded', () => {
    #                     console.log('DOMContentLoaded')
    #                     // Function to update the sandbox attribute
    #                     function updateIframeSandbox(iframe) {
    #                     console.log('updating iframe sandbox')
    #                         if (iframe.tagName === 'IFRAME') {
    #                             let sandboxAttr = iframe.getAttribute('sandbox') || '';
    #                             if (!sandboxAttr.includes('allow-top-navigation')) {
    #                                 iframe.setAttribute('sandbox', sandboxAttr + ' allow-top-navigation');
    #                             }
    #                         }
    #                     }

    #                     // Create a MutationObserver to detect added iframes
    #                     const observer = new MutationObserver((mutations) => {
    #                         mutations.forEach(mutation => {

    #                             if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {

    #                                 mutation.addedNodes.forEach(node => {
    #                                     console.log('we have a mutation!', node.tagName);
    #                                     if (node.tagName === 'IFRAME') {
    #                                         updateIframeSandbox(node);
    #                                     }
    #                                 });
    #                             }
    #                         });
    #                     });

    #                     // Ensure document.body is available before observing
    #                     const body = parent.document.body;
    #                     if (body) {
    #                         console.log('we have a body!');
    #                         observer.observe(body, {
    #                             childList: true,
    #                             subtree: true
    #                         });
    #                         console.log('observer set up', observer);
    #                         // Initially update existing iframes
    #                         const existingIframes = document.querySelectorAll('iframe');
    #                         console.log('existingIframes', existingIframes);
    #                         existingIframes.forEach(updateIframeSandbox);
    #                     } else {
    #                         console.error('document.body is not available');
    #                     }
    #             });
    #                 </script>
    #                 ''', height=0)

    # components.html('''<script language="javascript">
    #                 function observeIframeLoad(iframe) {
    #                     console.log('adding mutation observer to iframe');
    #                     const observer = new MutationObserver(() => {
    #                         console.log("running mutation observer");
    #                         // Add the sandbox attribute once content is about to load
    #                         let sandboxAttr = iframe.getAttribute('sandbox');
    #                         console.log('sandboxAttr', sandboxAttr);
    #                         // if (!sandboxAttr.includes('allow-top-navigation')) {
    #                         //    iframe.setAttribute('sandbox', sandboxAttr + ' allow-top-navigation');
    #                         // }
    #                         observer.disconnect(); // Stop observing once applied
    #                     });

    #                     observer.observe(iframe, { attributes: true, attributeFilter: ['sandbox'] });
    #                     console.log('observer', observer);
    #                 }

    #             // Apply the observer to each iframe
    #             const iframes = parent.document.querySelectorAll('iframe');
    #             console.log('setting up mutation observers');
    #             iframes.forEach(observeIframeLoad);
    #                 </script>
    #                 ''', height=0)

    # components.html('''<script language="javascript">
    #     var updateAndReloadIframes = function () {
    #         var reloadRequired = false;
    #         // Grab all iFrames, add the 'allow-top-navigation' property and reload them
    #         var iframes = parent.document.querySelectorAll("iframe");
    #         // console.log('iframes', iframes);
    #         console.log("checking for top navigation");
    #         for (var i = 0; i < iframes.length; i++) {
    #             if (!iframes[i].sandbox.contains('allow-top-navigation')) {
    #                 reloadRequired = true;
    #                 iframes[i].setAttribute("sandbox", "allow-forms allow-modals allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts allow-downloads allow-top-navigation-by-user-activation allow-top-navigation");
    #             }
    #         }
    #         if (reloadRequired) {
    #             setTimeout(function() {
    #                 for (var i = 0; i < iframes.length; i++) {
    #                     // iframes[i].contentWindow.location.reload();
    #                     iframes[i].contentDocument.location.reload();
    #                 }
    #             }, 300)
    #         }
    #     }
    #     updateAndReloadIframes()

    # </script>
    # ''', height=0)
