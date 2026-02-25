import express from 'express'
import cors from 'cors'
import dotenv from 'dotenv'
import attachmentRoutes from './routes/attachment.routes.js'

dotenv.config()

const app = express()

app.use(cors())
app.use(express.json())
app.use('/uploads', express.static('uploads'))

// Routes
app.use('/', attachmentRoutes)

export default app