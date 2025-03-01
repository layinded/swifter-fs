// This file is auto-generated by @hey-api/openapi-ts

export const Body_Authentication_login_userSchema = {
    properties: {
        grant_type: {
            anyOf: [
                {
                    type: 'string',
                    pattern: '^password$'
                },
                {
                    type: 'null'
                }
            ],
            title: 'Grant Type'
        },
        username: {
            type: 'string',
            title: 'Username'
        },
        password: {
            type: 'string',
            title: 'Password'
        },
        scope: {
            type: 'string',
            title: 'Scope',
            default: ''
        },
        client_id: {
            anyOf: [
                {
                    type: 'string'
                },
                {
                    type: 'null'
                }
            ],
            title: 'Client Id'
        },
        client_secret: {
            anyOf: [
                {
                    type: 'string'
                },
                {
                    type: 'null'
                }
            ],
            title: 'Client Secret'
        }
    },
    type: 'object',
    required: ['username', 'password'],
    title: 'Body_Authentication-login_user'
} as const;

export const HTTPValidationErrorSchema = {
    properties: {
        detail: {
            items: {
                '$ref': '#/components/schemas/ValidationError'
            },
            type: 'array',
            title: 'Detail'
        }
    },
    type: 'object',
    title: 'HTTPValidationError'
} as const;

export const MessageSchema = {
    properties: {
        message: {
            type: 'string',
            title: 'Message'
        }
    },
    type: 'object',
    required: ['message'],
    title: 'Message'
} as const;

export const NewPasswordSchema = {
    properties: {
        token: {
            type: 'string',
            title: 'Token'
        },
        new_password: {
            type: 'string',
            maxLength: 40,
            minLength: 8,
            title: 'New Password'
        }
    },
    type: 'object',
    required: ['token', 'new_password'],
    title: 'NewPassword'
} as const;

export const ProductSchema = {
    properties: {
        name: {
            type: 'string',
            maxLength: 255,
            title: 'Product Name'
        },
        description: {
            anyOf: [
                {
                    type: 'string'
                },
                {
                    type: 'null'
                }
            ],
            title: 'Product Description'
        },
        price: {
            type: 'number',
            minimum: 0,
            title: 'Product Price'
        },
        stock: {
            type: 'integer',
            minimum: 0,
            title: 'Stock Quantity'
        },
        id: {
            type: 'string',
            format: 'uuid',
            title: 'Id'
        }
    },
    type: 'object',
    required: ['name', 'price', 'stock'],
    title: 'Product'
} as const;

export const ProductCreateSchema = {
    properties: {
        name: {
            type: 'string',
            maxLength: 255,
            title: 'Product Name'
        },
        description: {
            anyOf: [
                {
                    type: 'string'
                },
                {
                    type: 'null'
                }
            ],
            title: 'Product Description'
        },
        price: {
            type: 'number',
            minimum: 0,
            title: 'Product Price'
        },
        stock: {
            type: 'integer',
            minimum: 0,
            title: 'Stock Quantity'
        }
    },
    type: 'object',
    required: ['name', 'price', 'stock'],
    title: 'ProductCreate'
} as const;

export const ProductUpdateSchema = {
    properties: {
        name: {
            anyOf: [
                {
                    type: 'string'
                },
                {
                    type: 'null'
                }
            ],
            title: 'Name'
        },
        description: {
            anyOf: [
                {
                    type: 'string'
                },
                {
                    type: 'null'
                }
            ],
            title: 'Description'
        },
        price: {
            anyOf: [
                {
                    type: 'number'
                },
                {
                    type: 'null'
                }
            ],
            title: 'Price'
        },
        stock: {
            anyOf: [
                {
                    type: 'integer'
                },
                {
                    type: 'null'
                }
            ],
            title: 'Stock'
        }
    },
    type: 'object',
    title: 'ProductUpdate'
} as const;

export const TokenSchema = {
    properties: {
        access_token: {
            type: 'string',
            title: 'Access Token'
        },
        refresh_token: {
            anyOf: [
                {
                    type: 'string'
                },
                {
                    type: 'null'
                }
            ],
            title: 'Refresh Token'
        },
        token_type: {
            type: 'string',
            title: 'Token Type',
            default: 'bearer'
        }
    },
    type: 'object',
    required: ['access_token'],
    title: 'Token'
} as const;

export const TokenRefreshRequestSchema = {
    properties: {
        refresh_token: {
            type: 'string',
            title: 'Refresh Token'
        }
    },
    type: 'object',
    required: ['refresh_token'],
    title: 'TokenRefreshRequest'
} as const;

export const TranslationCreateSchema = {
    properties: {
        language_code: {
            type: 'string',
            maxLength: 5,
            title: 'Language Code'
        },
        key: {
            type: 'string',
            maxLength: 255,
            title: 'Key'
        },
        value: {
            type: 'string',
            maxLength: 1000,
            title: 'Value'
        }
    },
    type: 'object',
    required: ['language_code', 'key', 'value'],
    title: 'TranslationCreate'
} as const;

export const TranslationCreateSchemaSchema = {
    properties: {
        language_code: {
            type: 'string',
            maxLength: 5,
            minLength: 2,
            title: 'Language Code',
            description: "Language code (e.g., 'en', 'cs')"
        },
        key: {
            type: 'string',
            maxLength: 255,
            minLength: 1,
            title: 'Key',
            description: 'Translation key'
        },
        value: {
            type: 'string',
            minLength: 1,
            title: 'Value',
            description: 'Translation value'
        }
    },
    type: 'object',
    required: ['language_code', 'key', 'value'],
    title: 'TranslationCreateSchema'
} as const;

export const TranslationPublicSchema = {
    properties: {
        language_code: {
            type: 'string',
            maxLength: 5,
            title: 'Language Code'
        },
        key: {
            type: 'string',
            maxLength: 255,
            title: 'Key'
        },
        value: {
            type: 'string',
            maxLength: 1000,
            title: 'Value'
        },
        id: {
            type: 'string',
            format: 'uuid',
            title: 'Id'
        }
    },
    type: 'object',
    required: ['language_code', 'key', 'value', 'id'],
    title: 'TranslationPublic'
} as const;

export const TranslationResponseSchema = {
    properties: {
        message: {
            type: 'string',
            title: 'Message'
        },
        translation: {
            '$ref': '#/components/schemas/TranslationPublic'
        }
    },
    type: 'object',
    required: ['message', 'translation'],
    title: 'TranslationResponse'
} as const;

export const TranslationUpdateSchema = {
    properties: {
        language_code: {
            anyOf: [
                {
                    type: 'string'
                },
                {
                    type: 'null'
                }
            ],
            title: 'Language Code'
        },
        key: {
            anyOf: [
                {
                    type: 'string'
                },
                {
                    type: 'null'
                }
            ],
            title: 'Key'
        },
        value: {
            anyOf: [
                {
                    type: 'string'
                },
                {
                    type: 'null'
                }
            ],
            title: 'Value'
        }
    },
    type: 'object',
    title: 'TranslationUpdate'
} as const;

export const UpdatePasswordSchema = {
    properties: {
        current_password: {
            type: 'string',
            maxLength: 40,
            minLength: 8,
            title: 'Current Password'
        },
        new_password: {
            type: 'string',
            maxLength: 40,
            minLength: 8,
            title: 'New Password'
        }
    },
    type: 'object',
    required: ['current_password', 'new_password'],
    title: 'UpdatePassword'
} as const;

export const UserCreateSchema = {
    properties: {
        email: {
            type: 'string',
            maxLength: 255,
            format: 'email',
            title: 'Email'
        },
        is_active: {
            type: 'boolean',
            title: 'Is Active',
            default: true
        },
        is_superuser: {
            type: 'boolean',
            title: 'Is Superuser',
            default: false
        },
        full_name: {
            anyOf: [
                {
                    type: 'string',
                    maxLength: 255
                },
                {
                    type: 'null'
                }
            ],
            title: 'Full Name'
        },
        preferred_language: {
            type: 'string',
            title: 'Preferred Language',
            default: 'en'
        },
        password: {
            anyOf: [
                {
                    type: 'string',
                    maxLength: 40,
                    minLength: 8
                },
                {
                    type: 'null'
                }
            ],
            title: 'Password'
        }
    },
    type: 'object',
    required: ['email'],
    title: 'UserCreate'
} as const;

export const UserPublicSchema = {
    properties: {
        email: {
            type: 'string',
            maxLength: 255,
            format: 'email',
            title: 'Email'
        },
        is_active: {
            type: 'boolean',
            title: 'Is Active',
            default: true
        },
        is_superuser: {
            type: 'boolean',
            title: 'Is Superuser',
            default: false
        },
        full_name: {
            anyOf: [
                {
                    type: 'string',
                    maxLength: 255
                },
                {
                    type: 'null'
                }
            ],
            title: 'Full Name'
        },
        preferred_language: {
            type: 'string',
            title: 'Preferred Language'
        },
        id: {
            type: 'string',
            format: 'uuid',
            title: 'Id'
        },
        auth_provider: {
            type: 'string',
            title: 'Auth Provider'
        },
        avatar_url: {
            anyOf: [
                {
                    type: 'string'
                },
                {
                    type: 'null'
                }
            ],
            title: 'Avatar Url'
        }
    },
    type: 'object',
    required: ['email', 'preferred_language', 'id', 'auth_provider'],
    title: 'UserPublic'
} as const;

export const UserRegisterSchema = {
    properties: {
        email: {
            type: 'string',
            maxLength: 255,
            format: 'email',
            title: 'Email'
        },
        password: {
            type: 'string',
            maxLength: 40,
            minLength: 8,
            title: 'Password'
        },
        full_name: {
            anyOf: [
                {
                    type: 'string',
                    maxLength: 255
                },
                {
                    type: 'null'
                }
            ],
            title: 'Full Name'
        }
    },
    type: 'object',
    required: ['email', 'password'],
    title: 'UserRegister'
} as const;

export const UserUpdateSchema = {
    properties: {
        email: {
            anyOf: [
                {
                    type: 'string',
                    maxLength: 255,
                    format: 'email'
                },
                {
                    type: 'null'
                }
            ],
            title: 'Email'
        },
        is_active: {
            type: 'boolean',
            title: 'Is Active',
            default: true
        },
        is_superuser: {
            type: 'boolean',
            title: 'Is Superuser',
            default: false
        },
        full_name: {
            anyOf: [
                {
                    type: 'string',
                    maxLength: 255
                },
                {
                    type: 'null'
                }
            ],
            title: 'Full Name'
        },
        preferred_language: {
            type: 'string',
            title: 'Preferred Language',
            default: 'en'
        },
        password: {
            anyOf: [
                {
                    type: 'string',
                    maxLength: 40,
                    minLength: 8
                },
                {
                    type: 'null'
                }
            ],
            title: 'Password'
        }
    },
    type: 'object',
    title: 'UserUpdate'
} as const;

export const UserUpdateMeSchema = {
    properties: {
        full_name: {
            anyOf: [
                {
                    type: 'string',
                    maxLength: 255
                },
                {
                    type: 'null'
                }
            ],
            title: 'Full Name'
        },
        email: {
            anyOf: [
                {
                    type: 'string',
                    maxLength: 255,
                    format: 'email'
                },
                {
                    type: 'null'
                }
            ],
            title: 'Email'
        },
        preferred_language: {
            anyOf: [
                {
                    type: 'string',
                    maxLength: 5
                },
                {
                    type: 'null'
                }
            ],
            title: 'Preferred Language'
        }
    },
    type: 'object',
    title: 'UserUpdateMe'
} as const;

export const UsersPublicSchema = {
    properties: {
        data: {
            items: {
                '$ref': '#/components/schemas/UserPublic'
            },
            type: 'array',
            title: 'Data'
        },
        count: {
            type: 'integer',
            title: 'Count'
        }
    },
    type: 'object',
    required: ['data', 'count'],
    title: 'UsersPublic'
} as const;

export const ValidationErrorSchema = {
    properties: {
        loc: {
            items: {
                anyOf: [
                    {
                        type: 'string'
                    },
                    {
                        type: 'integer'
                    }
                ]
            },
            type: 'array',
            title: 'Location'
        },
        msg: {
            type: 'string',
            title: 'Message'
        },
        type: {
            type: 'string',
            title: 'Error Type'
        }
    },
    type: 'object',
    required: ['loc', 'msg', 'type'],
    title: 'ValidationError'
} as const;