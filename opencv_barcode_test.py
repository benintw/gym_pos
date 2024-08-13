import cv2


def read_qrcode_from_webcam():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    # Initialize the QR code detector
    qr_decoder = cv2.QRCodeDetector()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Detect and decode the QR code
        data, bbox, _ = qr_decoder.detectAndDecode(frame)

        if bbox is not None and len(bbox) > 0:
            # Convert the bounding box points to integers and draw lines between them
            bbox = bbox.astype(int)

            for i in range(len(bbox)):
                # Draw lines between the points
                cv2.line(
                    frame,
                    tuple(bbox[i][0]),
                    tuple(bbox[(i + 1) % len(bbox)][0]),
                    (0, 255, 0),
                    2,
                )

            if data:
                # If the QR code contains data, display it
                cv2.putText(
                    frame,
                    data,
                    (bbox[0][0][0], bbox[0][0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (0, 255, 0),
                    2,
                )
                print(f"QR Code detected: {data}")

        # Display the resulting frame
        cv2.imshow("QR Code Scanner", frame)

        # Press 'q' to quit the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    read_qrcode_from_webcam()
