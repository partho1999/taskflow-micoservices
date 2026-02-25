import * as attachmentService from '../services/attachment.service.js'
import dotenv from 'dotenv'

dotenv.config()

// Get prefix from .env, default to /attachments
let ATTACHMENT_PREFIX = process.env.ATTACHMENT_PREFIX || '/attachments'
// Ensure it starts with '/'
if (!ATTACHMENT_PREFIX.startsWith('/')) ATTACHMENT_PREFIX = '/' + ATTACHMENT_PREFIX
// Remove trailing slash
ATTACHMENT_PREFIX = ATTACHMENT_PREFIX.replace(/\/$/, '')

export const uploadFile = async (req, res) => {
  try {
    const { entityType, entityId } = req.body

    if (!entityType || !entityId) {
      return res.status(400).json({ message: 'entityType and entityId are required' })
    }

    const file = req.file
    if (!file) {
      return res.status(400).json({ message: 'No file uploaded' })
    }

    // Save to DB
    const attachment = await attachmentService.createAttachment({
      filename: file.filename,
      original: file.originalname,
      mimetype: file.mimetype,
      size: file.size,
      path: file.path,
      entityType,
      entityId
    })

    // Build full URL dynamically
    const protocol = req.protocol
    const host = req.get('host')
    const fileUrl = `${protocol}://${host}${ATTACHMENT_PREFIX}/uploads/${file.filename}`

    res.status(201).json({ ...attachment, url: fileUrl })
  } catch (error) {
    console.error(error)
    res.status(500).json({ message: 'Upload failed' })
  }
}

export const getAll = async (req, res) => {
  try {
    const data = await attachmentService.getAllAttachments()

    const protocol = req.protocol
    const host = req.get('host')
    const result = data.map((item) => ({
      ...item,
      url: `${protocol}://${host}${ATTACHMENT_PREFIX}/uploads/${item.filename}`
    }))

    res.json(result)
  } catch (error) {
    console.error(error)
    res.status(500).json({ message: 'Failed to fetch attachments' })
  }
}

export const getByTypeAndEntity = async (req, res) => {
  try {
    const { entityType, entityId } = req.params
    const data = await attachmentService.getByTypeAndEntity(entityType, entityId)

    const protocol = req.protocol
    const host = req.get('host')
    const result = data.map((item) => ({
      ...item,
      url: `${protocol}://${host}${ATTACHMENT_PREFIX}/uploads/${item.filename}`
    }))

    res.json(result)
  } catch (error) {
    console.error(error)
    res.status(500).json({ message: 'Failed to fetch attachments' })
  }
}