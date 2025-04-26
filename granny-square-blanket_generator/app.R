library(shiny)
library(ggplot2)
library(colourpicker)


# Define Functions
generate_diagonal_pattern <- function(num_rows, num_cols, color_pairs) {
  pattern <- expand.grid(row = 1:num_rows, col = 1:num_cols)
  pattern$orientation <- ifelse((pattern$row + pattern$col) %% 2 == 0, "\\", "/")
  
  # Alternate colors for diagonal split
  pattern$color1 <- rep(color_pairs[[1]], length.out = nrow(pattern))
  pattern$color2 <- rep(color_pairs[[2]], length.out = nrow(pattern))
  
  return(pattern)
}

# Define UI
ui <- fluidPage(
    titlePanel("Granny Square Blanket Designer"),
    
    sidebarLayout(
        sidebarPanel(
            h4("Select Colors"),
            sliderInput("num_colors", "How many colors?", min = 1, max = 6, value = 6, step = 1),
            uiOutput("colorInputs"),  # Dynamic color inputs
            
            h4("Grid Settings"),
            numericInput("num_squares", "Total Number of Squares", value = 64, min = 6, max = 200),
            
            uiOutput("gridDimensions"),  # Dynamically adjust grid width and height
            
            h4("Square Layout"),
            radioButtons("square_layout", "Choose layout:",
                         choices = c("Monochromatic" = "mono",
                                     "Diagonal Split" = "diagonal"),
                         selected = "mono"),
            
            actionButton("generate", "Generate Blanket")
        ),
        
        mainPanel(
            plotOutput("gridPlot")
        )
    )
)

# Define Server
server <- function(input, output, session) {
    
    # Dynamically generate color input fields
    output$colorInputs <- renderUI({
        color_inputs <- list()
        default_colors <- c("#FFD700", "#228B22", "#1E90FF", "#FF69B4")  # Default yellow, green, blue, rose
        
        for (i in 1:input$num_colors) {
            color_inputs[[i]] <- colourInput(
                paste0("color", i),
                paste("Color", i),
                value = default_colors[i]
            )
        }
        do.call(tagList, color_inputs)
    })
    
    # Dynamically generate width and height inputs based on total squares
    output$gridDimensions <- renderUI({
      num_squares <- input$num_squares
      
      # Generate integer divisors of num_squares
      divisors <- seq(1, num_squares)[num_squares %% seq(1, num_squares) == 0]
      possible_dims <- unique(cbind(divisors, num_squares / divisors))
      
      # Create dropdown with valid dimensions
      selectInput(
        "grid_size", 
        "Select Grid Dimensions (Width x Height)",
        choices = apply(possible_dims, 1, function(x) paste(x[1], "x", x[2])),
        selected = paste(6, "x", 6)
      )
    })
    
    # Generate the grid
    generate_grid <- eventReactive(input$generate, {
        selected_colors <- sapply(1:input$num_colors, function(i) input[[paste0("color", i)]])
        selected_colors <- selected_colors[selected_colors != ""]
        
        # Extract width and height from the selected grid dimensions
        grid_dims <- as.numeric(unlist(strsplit(input$grid_size, " x ")))
        width <- grid_dims[1]
        height <- grid_dims[2]
        
        # Generate color assignments based on layout choice
        grid_data <- expand.grid(x = 1:width, y = 1:height)
        
        if (input$square_layout == "mono") {
            # Monochromatic squares
            grid_data$color1 <- sample(selected_colors, nrow(grid_data), replace = TRUE)
            grid_data$color2 <- grid_data$color1  # No second color
            
        } else if (input$square_layout == "diagonal") {
          # Diagonal split pattern
          grid_dims <- as.numeric(unlist(strsplit(input$grid_size, " x ")))
          num_rows <- grid_dims[2]
          num_cols <- grid_dims[1]
          
          # Use the first two selected colors for the diagonal pattern
          if (length(selected_colors) < 2) {
            stop("Please select at least two colors for a diagonal pattern.")
          }
          diagonal_colors <- list(selected_colors[1], selected_colors[2])
          
          # Generate diagonal pattern
          grid_data <- generate_diagonal_pattern(num_rows, num_cols, diagonal_colors)
        }
        
        return(grid_data)
    })
    
    # Render the blanket grid
    output$gridPlot <- renderPlot({
      grid_data <- generate_grid()
      
      # Extract grid dimensions
      grid_dims <- as.numeric(unlist(strsplit(input$grid_size, " x ")))
      num_rows <- grid_dims[2]
      num_cols <- grid_dims[1]
      
      if (input$square_layout == "mono") {
        ggplot(grid_data) +
          geom_tile(aes(x = x, y = y, fill = color1), color = "black") +
          scale_fill_identity() +
          theme_minimal() +
          theme(axis.text = element_blank(),
                axis.title = element_blank(),
                panel.grid = element_blank()) +
          ggtitle("Blanket Layout") +
          coord_fixed()
      } else if (input$square_layout == "diagonal") {
        ggplot(grid_data) +
          geom_tile(aes(x = col, y = row), fill = NA, color = "black") +  # Outline
          geom_tile(
            data = grid_data[grid_data$orientation == "\\", ],
            aes(x = col, y = row, fill = color1),
            color = "black"
          ) +
          geom_tile(
            data = grid_data[grid_data$orientation == "/", ],
            aes(x = col, y = row, fill = color2),
            color = "black"
          ) +
          scale_fill_identity() +
          theme_minimal() +
          theme(axis.text = element_blank(),
                axis.title = element_blank(),
                panel.grid = element_blank()) +
          ggtitle("Diagonal Split Blanket Layout") +
          coord_fixed()
      }
      
    })
    
    
}

# Run the application 
shinyApp(ui = ui, server = server)


