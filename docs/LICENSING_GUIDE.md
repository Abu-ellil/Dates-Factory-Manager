# Licensing System Guide 🔒

Your application is now protected by a **Hardware-Locked Licensing System**.

## How it Works

1.  **Customer installs the app**.
2.  **App asks for Activation**: On first run, it shows a "Machine ID" (e.g., `1AED-7CAA-D57F-993E`).
3.  **Customer sends you the ID**.
4.  **You generate a Key**: You use the `admin_keygen.py` tool.
5.  **Customer enters Key**: The app verifies it and unlocks.

## How to Generate Keys

You have a private tool in `bin/admin_keygen.py`.

1.  Open a terminal in your project folder.
2.  Run the tool:
    ```bash
    python bin/admin_keygen.py
    ```
3.  Enter the **Machine ID** the customer gave you.
4.  (Optional) Enter customer name and expiration date.
5.  **Copy the generated Key** and send it to the customer.

## Security Notes

-   **SECRET_KEY**: The security relies on the `SECRET_KEY` in `src/license_manager.py`.
    -   **CHANGE THIS KEY** before you sell!
    -   Make it a long, random string.
    -   If you change it later, all old keys will stop working (good for forcing upgrades, bad for existing users).

-   **Admin Tool**: Never give `admin_keygen.py` to customers. Keep it safe.

## Files

-   `src/license_manager.py`: Core logic (keep secret).
-   `bin/admin_keygen.py`: Key generator (keep private).
-   `src/templates/activate.html`: Activation screen.
-   `license.key`: File created on user's machine after activation.

## Trial Version?

Currently, the system enforces **Strict Activation** (app won't work without a key).
If you want a trial version (e.g., 7 days free), we would need to modify `license_manager.py` to allow a grace period.
