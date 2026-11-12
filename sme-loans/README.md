# Business Loans PH — HTML prototype
[Open the interactive prototype](https://shmalfus.github.io/experiments/sme-loans/)

For local use, open index.html in a browser. Run `python3 build.py` to create the self-contained Business-Loans-PH.html file and source archive. No server is required.

## Flow
- Borrow money → amount calculator.
- ₱5,000–₱49,999 → personal financial goals → product options.
- ₱50,000–₱600,000, inclusive → personal needs / business needs.
- Personal needs → financial goals → product options.
- Business needs → registration question.
- Registered → business purpose → monthly figures → original Flow placeholder.
- Not registered → registration requirement and personal options → personal financial goals.

The amount can be changed with the on-screen keypad or a physical keyboard. Digits append to the existing amount: 25,000 + 0 → 250,000. Use Backspace to delete or Ctrl/Cmd+A to replace the amount. Back preserves choices.

This is a prototype. No data is sent, no loan is submitted, and nothing is stored on a server. Investment and the following product applications are outside the supplied section; their buttons open an explanatory panel.

## Source
Figma file jJAEcvp7Oy3yxTtxu5BGVx, section 995:35758, Flow MVP.
The screen layout, copy, illustrations, icons, spacing, and reusable UI elements are implemented from the source frames. Poppins, Retail and Retail Text are embedded locally. The two purpose-selection variants use the same layout so the cards do not change size when switching selection.

## Verification
Both branches, unregistered-business fallback, inclusive threshold bounds, invalid amount handling, required fields, preserved amount on return, image loading, and a 360×800 viewport are checked using verify.py.

Purpose and business-purpose screens start without a selection or Continue button. Continue appears after selection. Financial-goal chips use dark selected styling; the footer stays visible while the content scrolls.

The registration requirement screen follows Figma 728:17256, including the selected folder illustration and updated copy.
