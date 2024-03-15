from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_pdf_with_margins(output_filename):
    # Define the page size and margins
    page_width, page_height = letter
    left_margin = 5
    top_margin = 6
    right_margin = 7
    bottom_margin = 10

    # Create a canvas with the specified output filename and page size
    c = canvas.Canvas(output_filename, pagesize=letter)

    # No need to draw a rectangle to visualize the margins for the final implementation
    # Just ensure the content is within the drawable area

    # Calculate the starting point for the text
    # The coordinate (0, 0) is at the bottom-left corner in ReportLab
    start_x = left_margin
    start_y = page_height - top_margin  # Start from the top, inside the margin

    # Position the text inside the margins
    c.drawString(start_x, start_y - 12, "This text is positioned inside the margins.")
    # Note: Subtracted 12 from start_y to move the text down a bit from the very top margin, adjust as needed

    # Save the PDF
    c.showPage()
    c.save()


# Generate the PDF with specified margins
create_pdf_with_margins("pdf_with_margins.pdf")
